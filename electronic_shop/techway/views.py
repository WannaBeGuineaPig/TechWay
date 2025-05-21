from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
import requests, datetime as dt
from python_moduls.add_product_data import *
from python_moduls.modul import *

URL_API = 'http://127.0.0.1:8000/api/'

def update_product_list(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        response_product_list = requests.get(URL_API + f'product_list/?sort={request.GET["sort"]}')
        product_list = calculate_feedback_and_set_image(response_product_list.json(), 'rating_sum', 'rating_count')

        render_page = render(request, 'techway\\product_previews_list.html', context={'product_list' : product_list})
        return JsonResponse({
            'result' : True,
            'product_list_page' : render_page.content.decode("utf-8")
        })
    
def main_window(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки главной страницы.
    '''
    if request.method == 'GET':
        response_product_list = requests.get(URL_API + 'product_list/' + (f'?iduser={request.session["id_user"]}' if 'id_user' in request.session else ''))
        product_list = response_product_list.json()
        product_list = calculate_feedback_and_set_image(response_product_list.json(), 'rating_sum', 'rating_count')

        return render(request, 'techway\\main_window.html', context={'product_list' : product_list})

def catalog_window(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки страницы с каталогом.
    '''
    if request.method == 'GET':
        return render(request, 'techway\\catalog.html')

def favorite_window(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки страницы с избранным.
    '''

    if 'id_user' not in request.session:
        return redirect('TechWay:home')

    if request.method == 'GET':
        return render(request, 'techway\\favorite.html')

def backet_window(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки страницы с корзиной.
    '''
    
    if 'id_user' not in request.session:
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

        requests.post(f'{URL_API}update_data_order/', data=json_data)

        return redirect('TechWay:home')

def personal_account_window(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки страницы с личным кабинетом.
    '''

    if 'id_user' not in request.session:
        return redirect('TechWay:home')
    
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

        else:
            return redirect('TechWay:home')

def authorization_window(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки страницы с авторизацией.
    '''
    if request.method == 'GET':
        return render(request, 'techway\\authorization.html')
    
    else:
        request.session['id_user'] = request.POST['id_user']
        return JsonResponse({"redirect_url" : redirect('TechWay:personal_account').url})

def registration_window(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки страницы с регистрацией.
    '''
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
    
def product_window(request: HttpRequest, product_id: int) -> HttpResponse:
    '''
    Представление для обработки страницы товара.
    '''
    if request.method == 'GET':
        return render(request, 'techway\\item_page.html')
    
def add_to_basket(request: HttpRequest, product_id: int):
    '''
    Представление для добавление в корзину.
    '''

    response = requests.get(f'{URL_API}add_to_basket/?id_user={request.session["id_user"]}&id_product={product_id}')

    return JsonResponse({"result" : response.status_code})
