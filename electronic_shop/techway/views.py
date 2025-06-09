import requests, base64
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.mail import EmailMultiAlternatives
from python_moduls.add_product_data import *
from python_moduls.pdf_files import *
from python_moduls.modul import *
from django.conf import settings
from django.templatetags.static import static
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

URL_API = 'http://127.0.0.1:8000/api/'

def send_to_mail(to_mail, pdf: str):
    html_content = render_to_string('techway\\mail.html', context={'check_pdf' : pdf})

    msg = EmailMultiAlternatives(
        "Ваш чек о заказе",
        '',
        settings.EMAIL_HOST_USER,
        [to_mail],
    )
    msg.attach_alternative(html_content, "text/html")

    photo_path = f'{os.path.dirname(__file__)}{static("techway/images/logo.png")}'
    
    with open(photo_path, 'rb') as f:
        image = MIMEImage(f.read())

    image.add_header('Content-ID', '<logo>')
    
    with open(pdf, 'rb') as file:
        content = MIMEApplication(file.read(), 'pdf', filename = 'check.pdf')

    content.add_header('Content-Disposition', 'attachment', filename='check.pdf')
    content.add_header('Content-ID', '<check>')

    msg.attach(image)
    msg.attach(content)

    try:
        msg.send()
    except:
        pass

def check_to_admin(id_user: int) -> bool:
    position = requests.get(f'{URL_API}auth_reg_user/{id_user}').json()['position']
    return position != 'Клиент'

def update_product_list(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        response_product_list = requests.get(URL_API + f'product_list/?sort={request.GET["sort"]}&' + (f'iduser={request.session["id_user"]}' if 'id_user' in request.session else '') + (f'&subcategory={request.GET["subcategory"]}' if 'subcategory' in request.GET else ''))
        product_list = calculate_feedback_and_set_image(response_product_list.json(), 'rating_sum', 'rating_count')

        render_page = render(request, 'techway\\product_previews_list.html', context={'product_list' : product_list})
        return JsonResponse({
            'result' : True,
            'product_list_page' : render_page.content.decode("utf-8")
        })
    
def main_view(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки главной страницы.
    '''

    if 'id_user' in request.session and check_to_admin(request.session['id_user']):
        return redirect('TechWay:admin_panel')
    
    if request.method == 'GET':
        id_user = f'iduser={request.session["id_user"]}' if 'id_user' in request.session else ''
        subcateory = ''
        categories = ''
        if 'subcategory' in request.session:
            subcateory = f'subcategory={request.session["subcategory"]}'
            categories = [*requests.get(f'{URL_API}categoty_section/?subcategory={request.session["subcategory"]}').json().values(), request.session["subcategory"]]
            request.session.pop('subcategory')

        check_two_varable = '&' if id_user != '' and subcateory != '' else ''
        response_product_list = requests.get(f'{URL_API}product_list/?{id_user}{check_two_varable}{subcateory}')
        product_list = response_product_list.json()
        product_list = calculate_feedback_and_set_image(response_product_list.json(), 'rating_sum', 'rating_count')

        return render(request, 'techway\\main_window.html', context={'product_list' : product_list, 'categories' : categories})

def catalog_view(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки страницы с каталогом.
    '''
    if 'id_user' in request.session and check_to_admin(request.session['id_user']):
        return redirect('TechWay:admin_panel')
    
    if request.method == 'GET':
        if 'subcategory' in request.GET:
            request.session['subcategory'] = request.GET['subcategory'] 
            return redirect('TechWay:home')

        elif 'category' in request.GET:
            all_categories = requests.get(f'{URL_API}subcategory_list_catalog/?category={request.GET["category"]}').json()
            select_categories = ['Каталог', request.GET['section'], request.GET['category']]
            return render(request, 'techway\\catalog.html', context={'all_categories' : all_categories, 'select_categories' : select_categories})
            
        elif 'section' in request.GET:
            all_categories = requests.get(f'{URL_API}category_list_catalog/?section={request.GET["section"]}').json()
            select_categories = ['Каталог', request.GET['section']]
            return render(request, 'techway\\catalog.html', context={'all_categories' : all_categories, 'select_categories' : select_categories})
        
        else:
            all_categories = requests.get(f'{URL_API}section_list/').json()
            select_categories = []

        return render(request, 'techway\\catalog.html', context={'all_categories' : all_categories, 'select_categories' : select_categories})

def favorite_view(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки страницы с избранным.
    '''

    if 'id_user' not in request.session:
        return redirect('TechWay:home')

    if check_to_admin(request.session['id_user']):
        return redirect('TechWay:admin_panel')

    if request.method == 'GET':
        return render(request, 'techway\\favorite.html', context={
            'favorites': requests.get(f'{URL_API}favorite_action/?id_user={request.session["id_user"]}').json()})

def backet_view(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки страницы с корзиной.
    '''
    
    if 'id_user' not in request.session or check_to_admin(request.session['id_user']):
        return redirect('TechWay:home')

    if request.method == 'GET':
        order_product = requests.get(f'{URL_API}basket_list/?id_user={request.session["id_user"]}')
        shop_list = requests.get(f'{URL_API}shop_list/')
        payment_method_list = [
            {'id_payment_method' : 1, 'method' : 'Наличными'},
            {'id_payment_method' : 2, 'method' : 'Картой'}
        ]
        return render(request, 'techway\\backet.html', context={
            'order_product': [] if order_product.status_code == 204 else order_product.json(),
            'shop_list' : shop_list.json(),
            'payment_method_list' : payment_method_list 
            })
    
    if request.method == 'POST':
        payment_method_list = [
            {'id_payment_method' : 1, 'method' : 'Наличными'},
            {'id_payment_method' : 2, 'method' : 'Картой'}
        ]

        method = ''
        for i in payment_method_list:
            if i['id_payment_method'] == int(request.POST['select_payment_method']):
                method = i['method']
                break

        json_data = {
            'id_user' : request.session['id_user'],
            'status' : 'Оформлен',
            'payment_method' : method,
            'id_shop' : request.POST['select_shop'],
        }

        receive_order = requests.post(f'{URL_API}update_data_order/', data=json_data)

        if receive_order.status_code == 400:
            order_product = requests.get(f'{URL_API}basket_list/?id_user={request.session["id_user"]}')
            shop_list = requests.get(f'{URL_API}shop_list/')
            payment_method_list = [
                {'id_payment_method' : 1, 'method' : 'Наличными'},
                {'id_payment_method' : 2, 'method' : 'Картой'}
            ]
            return render(request, 'techway\\backet.html', context={
                'order_product': [] if order_product.status_code == 204 else order_product.json(),
                'shop_list' : shop_list.json(),
                'payment_method_list' : payment_method_list,
                **receive_order.json()
            })

        receive_order = receive_order.json()
        response = requests.get(f'{URL_API}receive_cleared_products/?id_order={receive_order["idorder"]}').json()
        shop = requests.get(f'{URL_API}shop_list/?idshop={request.POST["select_shop"]}').json()[0]['addres']
        
        path_file_check = create_check_order(shop, receive_order['idorder'], method, response['date_ordering'], response['list_product'])
        
        email_user = requests.get(f'{URL_API}auth_reg_user/{request.session["id_user"]}').json()['mail']

        send_to_mail(email_user, path_file_check)

        delete_pdf_file()

        return redirect('TechWay:home')

def personal_account_view(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки страницы с личным кабинетом.
    '''

    if 'id_user' not in request.session:
        return redirect('TechWay:home')
    
    if check_to_admin(request.session['id_user']):
        return redirect('TechWay:admin_panel')
    
    if request.method == 'GET':
        user_dict = requests.get(URL_API + f'auth_reg_user/{request.session["id_user"]}').json()
        new_type_birthdate = user_dict['birthdate'].split('T')[0]
        user_dict.setdefault('new_type_birthdate', new_type_birthdate)
        return render(request, 'techway\\personal_account.html', context=user_dict)
    
    else:
        if 'btn' in request.POST and request.POST['btn'] == 'Выйти из аккаунта':
            request.session.pop('id_user')
            return redirect('TechWay:home')
        
        elif 'btn' in request.POST and request.POST['btn'] == 'Изменить':
            json_data = {
                'iduser': request.session['id_user'],
                'mail': request.POST['input_mail'],
                'lastname': request.POST['input_last_name'],
                'firstname': request.POST['input_first_name'],
                'midlename': request.POST['input_midle_name'],
                'birthdate': request.POST['input_birthdate'],
                'phone_number': request.POST['input_phone_number'],
                'password': request.POST['input_password'],
                'new_password': request.POST['input_password_update'],
            }
            user = requests.put(URL_API + 'auth_reg_user/', data=json_data)
            json_data.setdefault('new_type_birthdate', json_data['birthdate'].split('T')[0])    
            json_data.setdefault('error', user.content.decode('UTF-8')) if user.status_code == 409 else json_data.setdefault('complete', 'Данные успешно изменены!') 
                
            return render(request, 'techway\\personal_account.html', context=json_data)
                
        
        elif 'btn' in request.POST and request.POST['btn'] == 'Удалить аккаунт':
            requests.delete(URL_API + 'auth_reg_user/', data={'iduser': request.session['id_user']})
            request.session.pop('id_user')
            return redirect('TechWay:home')
        
        elif 'btn' in request.POST and request.POST['btn'] == 'История':
            return redirect('TechWay:history_order')

        else:
            return redirect('TechWay:home')

def authorization_view(request: HttpRequest) -> HttpResponse | JsonResponse:
    '''
    Представление для обработки страницы с авторизацией.
    '''

    if 'id_user' in request.session:
        return redirect('TechWay:home')

    if request.method == 'GET':
        return render(request, 'techway\\authorization.html')
    
    else:
        request.session['id_user'] = request.POST['iduser']
        url = redirect('TechWay:personal_account').url if request.POST['position'] == 'Клиент' else redirect('TechWay:admin_panel').url
        return JsonResponse({"redirect_url" : url})

def registration_view(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки страницы с регистрацией.
    '''
    if 'id_user' in request.session:
        return redirect('TechWay:home')
    
    if request.method == 'GET':
        return render(request, 'techway\\registration.html')
    
    else:
        dict_data = {
            'lastname' : request.POST['input_last_name'],
            'firstname' : request.POST['input_first_name'],
            'birthdate' : request.POST['input_birthdate'],
            'mail' : request.POST['input_mail'],
            'password' : request.POST['input_password']
        }
        response_user_create = requests.post(URL_API + 'auth_reg_user/', data=dict_data)
        
        if response_user_create.status_code == 409:
            dict_data.setdefault('password_confirm', request.POST['input_password_confirm'])
            errror = [f'{translate_text(i).capitalize()}: {translate_text(response_user_create.json()[i][0]).lower()}' for i in response_user_create.json()]
            dict_data.setdefault(f'error', errror[0])
            return render(request, 'techway\\registration.html', context={'dict_data' : dict_data})
    
        return redirect('TechWay:auth')
    
def product_view(request: HttpRequest, product_id: int) -> HttpResponse:
    '''
    Представление для обработки страницы товара.
    '''
    if 'id_user' in request.session and check_to_admin(request.session['id_user']):
        return redirect('TechWay:admin_panel')
    
    if request.method == 'GET':
        id_user = f'?id_user={request.session["id_user"]}' if 'id_user' in request.session else ''
        product = requests.get(f'{URL_API}get_product/{product_id}{id_user}').json()
        product['feedback'] = round(product['rating_sum'] / product['rating_count'], 2) if product['rating_count'] != 0 else 0
        return render(request, 'techway\\item_page.html', context={'product' : product})
    
def add_to_basket(request: HttpRequest, product_id: int) -> JsonResponse:
    '''
    Представление для добавление в корзину.
    '''
    response = requests.get(f'{URL_API}add_to_basket/?id_user={request.session["id_user"]}&id_product={product_id}')

    return JsonResponse({"status_code" : response.status_code, **response.json()})

def delete_item_basket(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        delete_item = requests.delete(f'{URL_API}change_order_product/', data={'list_id_product' : request.GET['list_id_product'], 'id_user' : request.session['id_user']})
        if delete_item.status_code == 404:
            return JsonResponse({'result' : False, **delete_item.json()})
        
        order_product = requests.get(f'{URL_API}basket_list/?id_user={request.session["id_user"]}')
        render_basket_list = render(request, 'techway\\backet_list_view.html', {'order_product' : [] if order_product.status_code == 204 else order_product.json()})
        return JsonResponse({'result' : True, 'render_basket_list' : render_basket_list.content.decode('UTF-8')})
    
def change_data_basket(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        id_user = request.session['id_user']
        change_item = requests.put(f'{URL_API}change_order_product/', data={
            'id_product' : request.GET['id_product'], 
            'id_user' : id_user,
            'amount_item' : request.GET['amount_item']
        })

        if change_item.status_code == 204:
            order_product = requests.get(f'{URL_API}basket_list/?id_user={id_user}')
            order_product = [] if order_product.status_code == 204 else order_product.json()
            render_basket_list = render(request, 'techway\\backet_list_view.html', {'order_product' : order_product})
            return JsonResponse({'result' : True, 'render_basket_list' : render_basket_list.content.decode('UTF-8')})
        else:
            return JsonResponse({'result' : False})
        

def admin_panel_view(request: HttpRequest):
    if 'id_user' not in request.session or not check_to_admin(request.session['id_user']):
        return redirect('TechWay:home')
    
    if request.method == 'GET':
        admin = requests.get(f'{URL_API}auth_reg_user/{request.session["id_user"]}').json()
        return render(request, 'techway\\admin_page.html', context={'position' : admin['position']})
    

def get_list_data_admin(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        list_items = []
        match request.GET['table']:
            case 'items':
                list_items = requests.get(f'{URL_API}product_list_admin_panel/').json()

            case 'orders':
                if 'start_period' in request.GET and 'stop_period' in request.GET:
                    list_items = requests.get(f'{URL_API}order_list_admin_panel/?start_period={request.GET["start_period"]}&stop_period={request.GET["stop_period"]}').json()
                else:
                    list_items = requests.get(f'{URL_API}order_list_admin_panel/').json()
            
            case 'employees':
                list_items = requests.get(f'{URL_API}employee_list_admin_panel/?id_user={request.session["id_user"]}').json()

        return JsonResponse({'table_data' : render(request, 'techway\\table_data_admin_panel.html', context={'list_items' : list_items}).content.decode()})
    
def update_status_order(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        requests.post(f'{URL_API}update_status_order_admin_panel/', {
            'status' : request.GET['new_status'],
            'id_order' : request.GET['id_order'],
        })
        return JsonResponse({'result' : True})


def personal_account_admin_view(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки страницы с личным кабинетом.
    '''

    if 'id_user' not in request.session or not check_to_admin(request.session['id_user']):
        return redirect('TechWay:home')
    
    if request.method == 'GET':
        user_dict = requests.get(URL_API + f'auth_reg_user/{request.session["id_user"]}').json()
        new_type_birthdate = user_dict['birthdate'].split('T')[0]
        user_dict.setdefault('new_type_birthdate', new_type_birthdate)
        return render(request, 'techway\\personal_account_admin.html', context=user_dict)
    
    else:
        if 'btn' in request.POST and request.POST['btn'] == 'Выйти из аккаунта':
            request.session.pop('id_user')
            return redirect('TechWay:admin_panel')
        
        elif 'btn' in request.POST and request.POST['btn'] == 'Изменить':
            json_data = {
                'iduser': request.session['id_user'],
                'mail': request.POST['input_mail'],
                'lastname': request.POST['input_last_name'],
                'firstname': request.POST['input_first_name'],
                'midlename': request.POST['input_midle_name'],
                'birthdate': request.POST['input_birthdate'],
                'phone_number': request.POST['input_phone_number'],
                'password': request.POST['input_password'],
                'new_password': request.POST['input_password_update'],
            }
            user = requests.put(URL_API + 'auth_reg_user/', data=json_data)
            json_data.setdefault('new_type_birthdate', json_data['birthdate'].split('T')[0])    
            json_data.setdefault('error', user.content.decode('UTF-8')) if user.status_code == 409 else json_data.setdefault('complete', 'Данные успешно изменены!') 
                
            return render(request, 'techway\\personal_account_admin.html', context=json_data)
                
        elif 'btn' in request.POST and request.POST['btn'] == 'Удалить аккаунт':
            requests.delete(URL_API + 'auth_reg_user/', data={'iduser': request.session['id_user']})
            request.session.pop('id_user')
            return redirect('TechWay:admin_panel')

        else:
            return redirect('TechWay:admin_panel')
        
def create_report_admin_panel(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        start_period = request.GET['start_period']
        stop_period = request.GET['stop_period']
        all_sum, items = requests.get(f'{URL_API}list_for_report_admin_panel/?start_period={start_period}&stop_period={stop_period}').json().values()
        path_file = create_report(start_period, stop_period, all_sum, items)
        pdf_data = ''
        with open(path_file, 'rb') as pdf_file:
            pdf_data = pdf_file.read()

        delete_pdf_file()

        return JsonResponse({'pdf_data' : base64.b64encode(pdf_data).decode('utf-8')})
    
def delete_admin_panel(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        if request.GET['table'] == 'items':
            response = requests.get(f'{URL_API}update_status_item_admin_panel/?id_item={request.GET["id"]}&status=Снят с продажи')
            
        else:
            response = requests.get(f'{URL_API}update_status_employee_admin_panel/?id_employee={request.GET["id"]}&status=Удалён')

        return JsonResponse({'new_status' : response.json()['status']})

def add_change_data(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        request.session['table'] = request.GET['table']
        request.session['id'] = request.GET["id"]

        return JsonResponse({'url' : redirect('TechWay:add_change').url})

def add_change_data_view(request: HttpRequest) -> JsonResponse:
    if request.method == 'GET':
        table = request.session['table']
        id = request.session['id']
        if table == 'items':
            data = {
                **requests.get(f'{URL_API}get_set_data_product/?id_product={id}').json(),
                'subcategory_list' : requests.get(f'{URL_API}subcategory_list/').json(),
                'manufacturer_list' : requests.get(f'{URL_API}manufacturer_list/').json(),
                'color_list' : requests.get(f'{URL_API}color_list/').json(),
                'type_display_list' : requests.get(f'{URL_API}type_display_list/').json(),
                'video_card_list' : requests.get(f'{URL_API}video_card_list/').json(),
                'processor_list' : requests.get(f'{URL_API}processor_list/').json(),
            }

        else:
            data = requests.get(f'{URL_API}get_set_data_employee/?id_employee={id}').json()
        
        return render(request, 'techway\\add_change_data.html', context={**data, 'table' : table})

    else:
        if request.session['table'] == 'items':
            response = requests.post(f'{URL_API}get_set_data_product/', data={
                'id_product' : request.POST['id_item'],
                'id_subcategory' : request.POST['select_subcategory'],
                'id_manufacturer' : request.POST['select_manufacturer'],
                'id_color' : request.POST['select_color'],
                'name' : request.POST['name_item'],
                'describe' : request.POST['describe_item'],
                'amount' : request.POST['amount_item'],
                'price' : request.POST['price_item'],
                'status' : request.POST['select_status'],
                'id_type_display' : request.POST['select_type_display'],
                'id_video_card' : request.POST['select_video_card'],
                'id_processor' : request.POST['select_processor'],
                'display_brightness' : request.POST['display_brightness'],
                'maximum_screen' : request.POST['maximum_screen'],
                'screen_diagonal' : request.POST['screen_diagonal'],
                'ram_memory' : request.POST['ram_amount'],
                'internal_memory' : request.POST['internal_memory'],
                'thickness' : request.POST['thickness'],
                'width' : request.POST['width'],
                'height' : request.POST['height'],
                'weight' : request.POST['weight'],
            })

        else:
            data = {
                'iduser' : request.POST['id_employee'],
                'status' : request.POST['select_status'],
                'position' : request.POST['select_position'],
                'lastname' : request.POST['lastname_employee'],
                'firstname' : request.POST['firstname_employee'],
                'midlename' : request.POST['midlename_employee'],
                'birthdate' : request.POST['birthdate_employee'],
                'phone_number' : request.POST['phone_number_employee'],
            }
            if 'mail_employee' in request.POST and 'password_employee' in request.POST:
                data = {
                    **data, 
                    'mail' : request.POST['mail_employee'],
                    'password' : request.POST['password_employee'],
                }
            response = requests.post(f'{URL_API}get_set_data_employee/', data=data)

        if response.status_code == 409:
            if request.session['table'] == 'items':
                data = {
                    **requests.get(f'{URL_API}get_set_data_product/?id_product={request.session["id"]}').json(),
                    'subcategory_list' : requests.get(f'{URL_API}subcategory_list/').json(),
                    'manufacturer_list' : requests.get(f'{URL_API}manufacturer_list/').json(),
                    'color_list' : requests.get(f'{URL_API}color_list/').json(),
                }
                data['id_subcategory'] = int(request.POST['select_subcategory'])
                data['id_manufacturer'] = int(request.POST['select_manufacturer'])
                data['id_color'] = int(request.POST['select_color'])
                data['name'] = request.POST['name_item']
                data['describe'] = request.POST['describe_item']
                data['amount'] = request.POST['amount_item']
                data['price'] = request.POST['price_item']
                data['status'] = request.POST['select_status']
            else:
                data = requests.get(f'{URL_API}get_set_data_employee/?id_employee={request.session["id"]}').json()
                data['status'] = request.POST['select_status']
                data['position'] = request.POST['select_position']
                data['lastname'] = request.POST['lastname_employee']
                data['firstname'] = request.POST['firstname_employee']
                data['midlename'] = request.POST['midlename_employee']
                data['birthdate'] = request.POST['birthdate_employee']
                data['phone_number'] = request.POST['phone_number_employee']

            return render(request, 'techway\\add_change_data.html', context={**data, 'table' : request.session['table'], 'errors' : [f'{translate_text(i).capitalize()}: {translate_text(response.json()[i][0]).lower()}' for i in response.json()]})

        request.session.pop('table')
        request.session.pop('id')
        return redirect('TechWay:admin_panel')
    

def history_order_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        list_data = requests.get(f'{URL_API}history_order_user/?id_user={request.session["id_user"]}').json()
        return render(request, 'techway\\history_orders.html', context={'list_data' : list_data})
    
def create_check_history_order(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        list_items = requests.get(f'{URL_API}order_product_for_check/?id_order={request.POST["id_order"]}').json()
        path_to_pdf = create_check_order(request.POST['id_order'], request.POST['address_shop'], request.POST['payment_method'], request.POST['date_ordering'], list_items)
        pdf_data = ''
        with open(path_to_pdf, 'rb') as pdf_file:
            pdf_data = pdf_file.read()

        delete_pdf_file()

        return JsonResponse({'pdf_data' : base64.b64encode(pdf_data).decode('utf-8')})
    

def add_favorite_item(request: HttpRequest):
    if request.method == 'GET':
        requests.post(f'{URL_API}favorite_action/', data={
            'id_user' : request.session["id_user"],
            'id_product' : request.GET["id_product"],
        })
        return JsonResponse({})

def delete_favorite_item(request: HttpRequest):
    if request.method == 'GET':
        requests.delete(f'{URL_API}favorite_action/', data={
            'id_user' : request.session["id_user"],
            'id_product' : request.GET["id_product"],
        })
        return JsonResponse({})