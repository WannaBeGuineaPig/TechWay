import pytz
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from .models import *
from .serializers import *
from python_moduls.modul import * 
from django.shortcuts import get_object_or_404
from django.db.models import F, Q
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.db.models import Sum

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ShopList(generics.ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

class OrderList(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class SubcategoryList(generics.ListAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer

class SectionList(generics.ListAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class ManufacturerList(generics.ListAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

class ColorList(generics.ListAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer

class TypeDisplayList(generics.ListAPIView):
    queryset = TypeDisplay.objects.all()
    serializer_class = TypeDisplaySerializer

class VideoCardList(generics.ListAPIView):
    queryset = VideoCard.objects.all()
    serializer_class = VideoCardSerializer

class ProcessorList(generics.ListAPIView):
    queryset = Processor.objects.all()
    serializer_class = ProcessorSerializer

class ProductList(APIView):
    def get(self, request: Request):
        product_list = Product.objects.all()

        if 'sort' in request.GET:        
            match(request.GET['sort']): 
                case 'low_cost_first':
                    product_list = product_list.order_by('price')

                case 'expensive_first':
                    product_list = product_list.order_by('-price')

                case 'number_of_feedback':
                    product_list = product_list.order_by('-rating_count')

                case 'best_feedback':
                    product_list = product_list.annotate(feedback=F('rating_sum') / F('rating_count')).order_by('-feedback')
        
        else:
            product_list = product_list.order_by('price')

        if 'subcategory' in request.GET:
            product_list = product_list.filter(id_subcategory=Subcategory.objects.filter(name=request.GET['subcategory']).first())

        if 'search' in request.GET:
            product_list = product_list.filter(Q(name__icontains=request.GET['search'])|Q(describe__icontains=request.GET['search']))

        count_page = len(product_list) // 10 + (0 if len(product_list) % 10 == 0 else 1)
        all_product_items = len(product_list)

        if 'number_page' in request.GET:
            number_page = int(request.GET['number_page']) - 1
            product_list = product_list[number_page*10:(number_page+1)*10]
        
        else:
            product_list = product_list[:10]

        list_data = ProductSerializer(product_list, many=True).data

        for item in range(len(list_data)):
            list_photo_item = ProductPhoto.objects.filter(id_product=list_data[item]['idproduct'])
            list_serializer = ProductPhotoSerializer(list_photo_item, many=True).data
            list_data[item]['url_photos'] = [i['url_photo'] for i in list_serializer]
            list_data[item]['feedback'] = round(list_data[item]['rating_sum'] / list_data[item]['rating_count'], 2) if list_data[item]['rating_count'] != 0 else 0

            if 'iduser' in request.GET:
                list_data[item]['favorites'] = len(Favorite.objects.filter(id_user=request.GET['iduser'], id_product=list_data[item]['idproduct'])) > 0
                order_product = Orderproduct.objects.filter(id_product=list_data[item]['idproduct'])
                order = Order.objects.filter(id_user=request.GET['iduser'], status='Не оформлен').first()
                order_product = [i for i in order_product if i.id_order == order]
                list_data[item]['basket'] = len(order_product) > 0

        return Response({'list_data' : list_data, 'count_page' : count_page, 'all_product_items' : all_product_items})

class AuthorizationRegistrationUser(APIView):
    def get(self, request: Request, pk = None):
        if pk:
            user = get_object_or_404(User, iduser=pk)
            return Response(UserSerializer(user).data)

        user = get_object_or_404(User, mail=request.GET['mail'], password=hash_password(request.GET['password']))
        if user.status == 'Удалён':
            return Response('Пользователь не найден!', status=status.HTTP_404_NOT_FOUND)

        return Response(UserSerializer(user).data)
    
    def post(self, request: Request):
        serializer = UserSerializer(data=request.POST, partial=True)
        if serializer.is_valid():
            serializer.save(status='Активен', position='Клиент', password=hash_password(request.POST['password']))
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


    def put(self, request: Request):
        user = get_object_or_404(User, iduser=request.data['iduser'])
        if hash_password(request.data['password']) != user.password:
            return Response(data='Не верный пароль!', status=status.HTTP_409_CONFLICT)

        if (check_user_mail:=User.objects.filter(mail=request.data['mail']).first()) != None and check_user_mail.iduser != user.iduser:
            return Response(data='Такая почта уже существует!', status=status.HTTP_409_CONFLICT)

        user.lastname = request.data['lastname']
        user.firstname = request.data['firstname']
        user.midlename = request.data['midlename']
        user.birthdate = request.data['birthdate']
        user.mail = request.data['mail']
        user.password = user.password if request.data['new_password'] == '' else hash_password(request.data['new_password'])
        user.phone_number = request.data['phone_number']
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    
    def delete(self, request: Request):
        user = get_object_or_404(User, iduser=request.data['iduser'])
        user.status = 'Удалён'
        user.save()
        return Response('Пользователь удалён!')


class AddToBasket(APIView):
    def get(self, request: Request):
        user = get_object_or_404(User, iduser=request.GET['id_user'])
        order = Order.objects.get_or_create(id_user=user, status='Не оформлен')
        product = Product.objects.filter(idproduct=request.GET['id_product']).first()
        if product.status == 'Снят с продажи':
            return Response({'error' : 'Товар снят с продажи!'}, status=status.HTTP_400_BAD_REQUEST)
        
        if product.amount <= 0:
            return Response({'error' : 'Товара нет в наличии!'}, status=status.HTTP_400_BAD_REQUEST)
        
        order_products = Orderproduct.objects.create(id_order=order[0], id_product=product, amount_product=1)
        order_products.save()
        return Response(OrderproductSerializer(order_products).data, status=status.HTTP_201_CREATED)
    
class BasketList(APIView):
    def get(self, request: Request):
        order = Order.objects.filter(id_user=request.GET['id_user'], status='Не оформлен').first()
        if order == None:
            return Response([], status=status.HTTP_204_NO_CONTENT)
        
        orderproduct = OrderproductSerializer(Orderproduct.objects.filter(id_order=order), many=True).data
        for item in orderproduct:
            product = get_object_or_404(Product, idproduct=item['id_product'])
            if product.amount < item['amount_product']:
                item['amount_product'] = product.amount

            item['product'] = ProductSerializer(Product.objects.get(idproduct=item['id_product'])).data
            list_photo_item = ProductPhoto.objects.filter(id_product=item['id_product'])
            list_serializer = ProductPhotoSerializer(list_photo_item, many=True).data
            item['product']['url_photo'] = list_serializer[0]['url_photo']
            item.pop('id_product')

        return Response(orderproduct)
    


class UpdateDataOrder(APIView):
    def post(self, request: Request):
        order = get_object_or_404(Order, id_user=get_object_or_404(User, iduser=request.POST['id_user']), status='Не оформлен')

        if 'status' in request.POST:
            order.status = request.POST['status']
            if request.POST['status'] == 'Оформлен':
                orderproduct = Orderproduct.objects.filter(id_order=order)
                for item in orderproduct:
                    product = item.id_product
                    product.amount -= item.amount_product
                    if product.status == 'Снят с продажи':
                        return Response({'error' : f'{product.name} снят с продажи'}, status=status.HTTP_400_BAD_REQUEST)

                    product.save()
                timezone.now()
                order.date_of_regestration = datetime.now(pytz.UTC)

        if 'id_shop' in request.POST:
            order.id_shop = get_object_or_404(Shop, idshop=request.POST['id_shop'])
        
        if 'payment_method' in request.POST:
            order.payment_method = request.POST['payment_method']

        order.save()

        return Response(OrderSerializer(order).data)

class ChangeOrderProduct(APIView):
    def put(self, request: Request):
        order = get_object_or_404(Order, id_user=get_object_or_404(User, iduser=request.data['id_user']), status='Не оформлен') 
        product = get_object_or_404(Product, idproduct=request.data['id_product'])
        orderproduct = Orderproduct.objects.filter(id_order=order, id_product=product).first()

        if orderproduct == None:
            return Response({'error' : 'Товар не найден!'}, status=status.HTTP_404_NOT_FOUND)
        
        if 'amount_item' not in request.data:
            return Response({'error' : 'Новое количества товара не найденно!'}, status=status.HTTP_404_NOT_FOUND)
        
        new_amount = int(request.data['amount_item'])
        if product.amount < new_amount:
            return Response({'error' : 'Новое количества товара не должно превышать максимальное возможное!'}, status=status.HTTP_400_BAD_REQUEST)
        
        orderproduct.amount_product = new_amount
        orderproduct.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


    def delete(self, request: Request):
        order = get_object_or_404(Order, id_user=get_object_or_404(User, iduser=request.data['id_user']), status='Не оформлен')
        for id_product in request.data['list_id_product'].split(' '):
            product = get_object_or_404(Product, idproduct=id_product)
            orderproduct = Orderproduct.objects.filter(id_order=order, id_product=product).first()
            if orderproduct == None:
                return Response({'error' : 'Товар не найден!'}, status=status.HTTP_404_NOT_FOUND)
            
            orderproduct.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class GetProduct(APIView):
    def get(self, request, id_product: int):
        def create_property(property: Property):
            type_display = property.id_type_display.name if property.id_type_display else ''
            video_card = property.id_video_card.name if property.id_video_card else ''
            processor = property.id_processor.name if property.id_processor else ''
            property = PropertySerializer(property).data
            property = {'type_display' : type_display, 'video_card' : video_card, 'processor' : processor, **property} 
            new_property = {}
            new_keys = {
                "display_brightness_cd_m_2_field": 'Яркость дисплея(cd/m^2)',
                "maximum_screen_frequency_hz_field": 'Максимальная частота(Гц)',
                "screen_diagonal_inch_field": 'Диагональ экрана(дюйм)',
                "ram_amount_gb_field": 'Количество оперативной памяти(гб)',
                "internal_memory_amount_gb_field": 'Количество встроенной памяти(гб)',
                "thickness_mm_field": 'Толщина(мм)',
                "width_mm_field": 'Ширина(мм)',
                "height_mm_field": 'Высота(мм)',
                "weight_kg_field": 'Вес(кг)',
                "type_display": 'Тип дисплея',
                "video_card": 'Тип видеокарты',
                "processor": 'Тип процессора'
            }
            check_list = ['idproperty', 'id_type_display', 'id_processor', 'id_video_card']
            for key, value in property.items():
                if value and key not in check_list:
                    new_property[new_keys[key]] = value

            return new_property

        product = get_object_or_404(Product, idproduct=id_product)
        subcategory = product.id_subcategory.name
        category = product.id_subcategory.id_category.name
        section = product.id_subcategory.id_category.id_section.name
        property = create_property(product.id_property)

        product = ProductSerializer(product).data
        list_photo_item = ProductPhoto.objects.filter(id_product=product['idproduct'])
        list_serializer = ProductPhotoSerializer(list_photo_item, many=True).data
        product = {**product, 'subcategory' : subcategory, 'category' : category, 'section' : section, 'property' : property, 'url_photos' : [i['url_photo'] for i in list_serializer]} 

        if 'id_user' in request.GET:
            product['favorites'] = len(Favorite.objects.filter(id_user=request.GET['id_user'], id_product=product['idproduct'])) > 0
            order_product = Orderproduct.objects.filter(id_product=product['idproduct'])
            order = Order.objects.filter(id_user=request.GET['id_user'], status='Не оформлен').first()
            order_product = [i for i in order_product if i.id_order == order]
            product['basket'] = len(order_product) > 0

        return Response(product)
    

class ReceiveClearedProducts(APIView):
    def get(self, request):
        order = get_object_or_404(Order, idorder=request.GET['id_order'], status='Оформлен')
        date_ordering = datetime.strftime(order.date_of_regestration.replace(hour=order.date_of_regestration.hour+5), '%Y-%m-%d %H:%M:%S')
        result_dict = {'id_order' : order.idorder, 'date_ordering' : date_ordering, 'list_product' : []}
        for item in Orderproduct.objects.filter(id_order=order):
            result_dict['list_product'].append({**ProductSerializer(item.id_product).data, 'amount' : item.amount_product})

        return Response(result_dict)
    
class ProductListAdminPanel(APIView):
    def get(self, request):
        def create_property_dict(data: Property) -> dict:
            return {
                "Тип дисплея": data.id_type_display.name if data.id_type_display != None else 'Нет',
                "Тип видеокарты": data.id_video_card.name if data.id_video_card != None else 'Нет',
                "Тип процессора": data.id_processor.name if data.id_processor != None else 'Нет',
                "Яркость дисплея(кд/м^2)": data.display_brightness_cd_m_2_field,
                "Частота экрана(Гц)": data.maximum_screen_frequency_hz_field,
                "Диагональ экрана(дюйм)": data.screen_diagonal_inch_field,
                "Количество оперативной памяти(гб)": data.ram_amount_gb_field,
                "Количество встроенной памяти(гб)": data.internal_memory_amount_gb_field,
                "Толщина(мм)": data.thickness_mm_field,
                "Ширина(мм)": data.width_mm_field,
                "Высота(мм)": data.height_mm_field,
                "Вес(кг)": data.weight_kg_field
            }

        products = Product.objects.all()
        list_products = []
        for item in products:
            list_products.append({
                "Номер товара": item.idproduct,
                "Свойства": create_property_dict(item.id_property),
                "Подкатегория": item.id_subcategory.name,
                "Производитель": item.id_manufacturer.name,
                "Цвет": item.id_color.name,
                "Название": item.name,
                "Описание": item.describe,
                "Цена": item.price,
                "Количество": item.amount,
                "Оценка": round(item.rating_sum / item.rating_count, 2) if item.rating_count != 0 else 0,
                "Статус": item.status
            })

        return Response(list_products)
    
class OrderListAdminPanel(APIView):
    def get(self, request):
        if 'start_period' in request.GET and 'stop_period' in request.GET:
            timezone.now()
            current_timezone = pytz.timezone(settings.TIME_ZONE)
            start_period = current_timezone.localize(datetime.strptime(request.GET["start_period"], "%Y-%m-%d"))
            stop_period = current_timezone.localize(datetime.strptime(request.GET["stop_period"], "%Y-%m-%d"))
            orders = Order.objects.filter(date_of_regestration__gte=start_period, date_of_regestration__lte=stop_period)
        
        else:
            orders = Order.objects.all()
        
        orders = orders.order_by('-date_of_regestration')
        list_orders = []

        for order in orders:
            sum_order = Orderproduct.objects.filter(id_order=order.idorder).aggregate(sum_order=Sum(F('id_product__price') * F('amount_product')))['sum_order']
            list_orders.append({
                "Номер заказа": order.idorder,
                "Почта пользователя": order.id_user.mail,
                "Адрес магазина": order.id_shop.addres if order.id_shop != None else 'Нет',
                "Сумма заказа": sum_order,
                "Тип оплаты": order.payment_method if order.payment_method != None else 'Нет',
                "Статус": order.status,
                "Дата регистрации заказа": 'Нет' if order.date_of_regestration == None else datetime.strftime(order.date_of_regestration + timedelta(hours=5), '%Y-%m-%d %H:%M:%S')
            })
        
        return Response(list_orders)
    
class EmployeeListAdminPanel(APIView):
    def get(self, request):
        employees = User.objects.exclude(position='Клиент').exclude(iduser=request.GET['id_user'])
        list_employees = []

        for employee in employees:
            list_employees.append({
                'Номер сотрудника' : employee.iduser,
                'Статус' : employee.status,
                'Должность' : employee.position,
                'Фамилия' : employee.lastname,
                'Имя' : employee.firstname,
                'Отчество' : employee.midlename if employee.midlename != None else '',
                'Дата рождения' : datetime.strftime(employee.birthdate, '%Y-%m-%d %H:%M:%S'),
                'Почта' : employee.mail,
                'Номер телефона' : employee.phone_number if employee.phone_number != None else ''
            })
        
        return Response(list_employees)
    

class UpdateStatusOrderAdminPanel(APIView):
    def post(self, request):
        if 'status' not in request.data:
            return Response({'error' : 'Не найден статус'}, status=status.HTTP_404_NOT_FOUND)
        
        if 'id_order' not in request.data:
            return Response({'error' : 'Не найден номер заказа'}, status=status.HTTP_404_NOT_FOUND)
        
        order = get_object_or_404(Order, idorder=request.data['id_order'])

        order.status = request.data['status']
        order.save()

        return Response(OrderSerializer(order).data)
    
class ListForReportAdminPanel(APIView):
    def get(self, request: Request):
        timezone.now()
        current_timezone = pytz.timezone(settings.TIME_ZONE)
        start_period = current_timezone.localize(datetime.strptime(request.GET["start_period"], "%Y-%m-%d"))
        stop_period = current_timezone.localize(datetime.strptime(request.GET["stop_period"], "%Y-%m-%d"))
        orders = Order.objects.filter(date_of_regestration__gte=start_period, date_of_regestration__lte=stop_period)

        list_items = []
        all_sum_orders = 0

        for order in orders:
            sum_order = Orderproduct.objects.filter(id_order=order.idorder).aggregate(sum_order=Sum(F('id_product__price') * F('amount_product')))['sum_order']
            all_sum_orders += sum_order
            list_items.append([
                order.id_user.iduser,
                order.idorder,
                datetime.strftime(order.date_of_regestration, '%Y-%m-%d %H:%M:%S'),
                sum_order,
                order.payment_method
            ])

        return Response({'all_sum_orders' : all_sum_orders, 'list_items' : list_items})
    

class UpdateStatusItemAdminPanel(APIView):
    def get(self, request):
        if 'status' not in request.GET:
            return Response({'error' : 'Не найден статус'}, status=status.HTTP_404_NOT_FOUND)
        
        if 'id_item' not in request.GET:
            return Response({'error' : 'Не найден номер товара'}, status=status.HTTP_404_NOT_FOUND)
        
        item = get_object_or_404(Product, idproduct=request.GET['id_item'])

        item.status = request.GET['status']
        item.save()

        return Response(ProductSerializer(item).data)
    
class UpdateStatusEmployeeAdminPanel(APIView):
    def get(self, request):
        if 'status' not in request.GET:
            return Response({'error' : 'Не найден статус'}, status=status.HTTP_404_NOT_FOUND)
        
        if 'id_employee' not in request.GET:
            return Response({'error' : 'Не найден номер сотрудника'}, status=status.HTTP_404_NOT_FOUND)
        
        employee = get_object_or_404(User, iduser=request.GET['id_employee'])

        employee.status = request.GET['status']
        employee.save()

        return Response(UserSerializer(employee).data)
    

class GetSetDataProduct(APIView):
    def get(self, request: Request):
        product = Product.objects.filter(idproduct=request.GET['id_product'])
        if len(product) == 0:
            return Response({'idproduct' : -1, 'status_list' : ['В продаже', 'Снят с продажи']})
        return Response({**ProductSerializer(product.first()).data, 
                        **PropertySerializer(product.first().id_property).data,
                        'status_list' : ['В продаже', 'Снят с продажи'],
                        })
    
    def post(self, request: Request):        
        def check_to_digit(content): 
            return content if content.isdigit() else None
        id_product = int(request.data['id_product'])

        type_display = TypeDisplay.objects.filter(idtype_display=int(request.data['id_type_display']))
        video_card = VideoCard.objects.filter(idvideo_card=int(request.data['id_video_card']))
        processor = Processor.objects.filter(idprocessor=int(request.data['id_processor']))
        data_property = {
            'id_type_display' : type_display.first() if len(type_display) > 0 else None,
            'id_video_card' : video_card.first() if len(video_card) > 0 else None,
            'id_processor' : processor.first() if len(processor) > 0 else None,
            'display_brightness_cd_m_2_field' : check_to_digit(request.data['display_brightness']),
            'maximum_screen_frequency_hz_field' : check_to_digit(request.data['maximum_screen']),
            'screen_diagonal_inch_field' : check_to_digit(request.data['screen_diagonal']),
            'ram_amount_gb_field' : check_to_digit(request.data['ram_memory']),
            'internal_memory_amount_gb_field' : check_to_digit(request.data['internal_memory']),
            'thickness_mm_field' : check_to_digit(request.data['thickness']),
            'width_mm_field' : check_to_digit(request.data['width']),
            'height_mm_field' : check_to_digit(request.data['height']),
            'weight_kg_field' : check_to_digit(request.data['weight']),
        }

        if id_product == -1:
            new_property = Property(**data_property)
            new_property.save()
            product = Product(
                id_property = new_property,
                id_subcategory = Subcategory.objects.get(idsubcategory=request.data['id_subcategory']),
                id_manufacturer = Manufacturer.objects.get(idmanufacturer=request.data['id_manufacturer']),
                id_color = Color.objects.get(idcolor=request.data['id_color']),
                name = request.data['name'],
                describe = request.data['describe'],
                price = request.data['price'],
                amount = request.data['amount'],
                rating_count = 0,
                rating_sum = 0,
                status = request.data['status']
            )
            product.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        product = Product.objects.get(idproduct=id_product)
        Property.objects.filter(idproperty=product.id_property.idproperty).update(**data_property)

        product.id_subcategory = Subcategory.objects.get(idsubcategory=request.data['id_subcategory'])
        product.id_manufacturer = Manufacturer.objects.get(idmanufacturer=request.data['id_manufacturer'])
        product.id_color = Color.objects.get(idcolor=request.data['id_color'])
        product.name = request.data['name']
        product.describe = request.data['describe']
        product.price = request.data['price']
        product.amount = request.data['amount']
        product.status = request.data['status']
        product.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class GetSetDataEmployee(APIView):
    def get(self, request: Request):
        employee = User.objects.filter(iduser=request.GET['id_employee'])
        if len(employee) == 0:
            return Response({'iduser' : -1, 'status_list' : ['Активен', 'Удалён'], 'position_list' : ['Сотрудник пункта выдачи', 'Сотрудник склада']})
        user_data = UserSerializer(employee.first()).data
        user_data['birthdate'] = user_data['birthdate'].split('T')[0]
        user_data['midlename'] = user_data['midlename'] if user_data['midlename'] != None else ''
        user_data['phone_number'] = user_data['phone_number'] if user_data['phone_number'] != None else ''
        return Response({**user_data, 
                        'status_list' : ['Активен', 'Удалён'],
                        'position_list' : ['Сотрудник пункта выдачи', 'Сотрудник склада'],
                        })
    
    def post(self, request: Request):
        serializer = UserSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
        
        id_employee = int(request.data['iduser'])
        current_timezone = pytz.timezone(settings.TIME_ZONE)
        
        if id_employee == -1:
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        employee = User.objects.get(iduser=id_employee)

        employee.position = request.data['position']
        employee.lastname = request.data['lastname']
        employee.firstname = request.data['firstname']
        employee.midlename = request.data['midlename']
        employee.birthdate = current_timezone.localize(datetime.strptime(request.data['birthdate'], '%Y-%m-%d'))

        employee.phone_number = request.data['phone_number']
        employee.status = request.data['status']

        employee.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class HistoryOrderUser(APIView):
    def get(self, request: Request):
        orders = OrderSerializer(Order.objects.filter(id_user=get_object_or_404(User, iduser=request.GET["id_user"])).exclude(status='Не оформлен').order_by('-idorder'), many=True).data
        for order in orders:
            shop = Shop.objects.filter(idshop=order['id_shop'])
            order['shop'] = shop.first().addres if len(shop) > 0 else 'Нет'
            date = 'Нет'
            if order['date_of_regestration'] != None:
                date = datetime.strptime(order['date_of_regestration'].split('+')[0], '%Y-%m-%dT%H:%M:%S')
                date += timedelta(hours=5)
                date = date.strftime('%Y-%m-%d %H:%M:%S')
            order['date_of_regestration'] = date


        return Response(orders)
    
class OrderProductForCheck(APIView):
    def get(self, request: Request):
        list_product = []
        for item in Orderproduct.objects.filter(id_order=get_object_or_404(Order, idorder=request.GET['id_order'])):
            list_product.append({**ProductSerializer(item.id_product).data, 'amount' : item.amount_product})
        return Response(list_product)
    
class SubcategoryListCatalog(APIView):
    def get(self, request: Request):
        subcategory_list = Subcategory.objects.filter(id_category=Category.objects.filter(name=request.GET['category']).first())
        return Response(SubcategorySerializer(subcategory_list, many=True).data)
    
class CategoryListCatalog(APIView):
    def get(self, request: Request):
        category_list = Category.objects.filter(id_section=Section.objects.filter(name=request.GET['section']).first())
        return Response(CategorySerializer(category_list, many=True).data)
    
class CategotySection(APIView):
    def get(self, request: Request):
        subcategory = Subcategory.objects.filter(name=request.GET['subcategory']).first()
        return Response({'section' : subcategory.id_category.id_section.name, 'category' : subcategory.id_category.name})
    
class FavoriteAction(APIView):
    def get(self, request: Request):
        user = get_object_or_404(User, iduser=request.GET['id_user'])
        favorite_list = Favorite.objects.filter(id_user=user)
        result_list = []
        for item in favorite_list:
            product = ProductSerializer(item.id_product).data
            product['url_image'] = ProductPhoto.objects.filter(id_product=item.id_product).first().url_photo
            order_product = Orderproduct.objects.filter(id_product=item.id_product)
            order = Order.objects.filter(id_user=user, status='Не оформлен').first()
            order_product = [i for i in order_product if i.id_order == order]
            product['basket'] = len(order_product) > 0
            product['feedback'] = round(item.id_product.rating_sum / item.id_product.rating_count, 2) if item.id_product.rating_count != 0 else 0
            result_list.append(product)
        
        return Response(result_list)

    def post(self, request: Request):
        Favorite.objects.create(id_user=get_object_or_404(User, iduser=request.data['id_user']), id_product=get_object_or_404(Product, idproduct=request.data['id_product']))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request: Request):
        Favorite.objects.get(id_user=get_object_or_404(User, iduser=request.data['id_user']), id_product=get_object_or_404(Product, idproduct=request.data['id_product'])).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RecoveryPassword(APIView):
    def post(self, request: Request):
        if 'mail' not in request.data:
            return Response('Не передана почта!', status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(mail=request.data['mail'])
        if len(user) == 0:
            return Response('Пользователь с такой почтой не найден!', status=status.HTTP_400_BAD_REQUEST)
        return Response(UserSerializer(user.first()).data, status=status.HTTP_200_OK)


class UpdatePassword(APIView):
    def post(self, request: Request):
        if 'password' not in request.data:
            return Response('Не передан пароль!', status=status.HTTP_400_BAD_REQUEST)
        
        if 'mail' not in request.data:
            return Response('Не передана почта!', status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(mail=request.data['mail'])

        if len(user) == 0:
            return Response('Пользователь с такой почтой не найден!', status=status.HTTP_400_BAD_REQUEST)
        
        user = user.first()

        user.password = hash_password(request.data['password'])
        user.save()
        return Response('Пароль успешно изменён!')