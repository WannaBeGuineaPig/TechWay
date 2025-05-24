from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from .models import *
from .serializers import *
from python_moduls.modul import * 
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.db.models import F
from datetime import datetime

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProductList(APIView):
    def get(self, request: Request):
        product_list = Product.objects.all()
        
        if 'sort' in request.GET:
        
            match(request.GET['sort']):
                case 'popular_first':
                    pass

                case 'low_cost_first':
                    product_list = product_list.order_by('price')

                case 'expensive_first':
                    product_list = product_list.order_by('-price')

                case 'number_of_feedback':
                    product_list = product_list.order_by('-rating_count')

                case 'best_feedback':
                    product_list = product_list.annotate(feedback=F('rating_sum') / F('rating_count')).order_by('-feedback')

        list_data = ProductSerializer(product_list, many=True).data

        for item in range(len(list_data)):
            list_photo_item = ProductPhoto.objects.filter(id_product=list_data[item]['idproduct'])
            list_serializer = ProductPhotoSerializer(list_photo_item, many=True).data
            list_data[item]['url_photos'] = [i['url_photo'] for i in list_serializer]

            if 'iduser' in request.GET:
                list_data[item]['favorites'] = len(Favorite.objects.filter(id_user=request.GET['iduser'], id_product=list_data[item]['idproduct'])) > 0
                order_product = Orderproduct.objects.filter(id_product=list_data[item]['idproduct'])
                order = Order.objects.filter(id_user=request.GET['iduser'], status='Не оформлен').first()
                order_product = [i for i in order_product if i.id_order == order]
                list_data[item]['basket'] = len(order_product) > 0
            

        return Response(list_data)

class AuthorizationRegistrationUser(APIView):
    def get(self, request: Request, pk = None):
        if pk:
            user = get_object_or_404(User, iduser=pk)

            return Response(model_to_dict(user))

        user = get_object_or_404(User, mail=request.GET['mail'], password=hash_password(request.GET['password']))
        if user.status == 'Удалён':
            return Response('Пользователь не найден!', status=status.HTTP_404_NOT_FOUND)

        return Response(model_to_dict(user))
    
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
        return Response(model_to_dict(user), status=status.HTTP_201_CREATED)
    
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
        if product.amount == 0:
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
            item['product'] = ProductSerializer(Product.objects.get(idproduct=item['id_product'])).data
            list_photo_item = ProductPhoto.objects.filter(id_product=item['id_product'])
            list_serializer = ProductPhotoSerializer(list_photo_item, many=True).data
            item['product']['url_photo'] = list_serializer[0]['url_photo']
            item.pop('id_product')

        return Response(orderproduct)
    
class ShopList(generics.ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

class UpdateDataOrder(APIView):
    def post(self, request: Request):
        
        def change_amount_product(list_items) -> list:
            for i  in list_items:
                item = Product.objects.filter(idproduct=i['id_product']).first()
                if item == None:
                    continue
                item.amount -= i['amount_product']
                item.save()

        order = get_object_or_404(Order, id_user=get_object_or_404(User, iduser=request.POST['id_user']), status='Не оформлен')

        if 'status' in request.POST:
            order.status = request.POST['status']
            if request.POST['status'] == 'Оформлен':
                order.payment_method = datetime.now()
                change_amount_product(OrderproductSerializer(Orderproduct.objects.filter(id_order=order), many=True).data)

        if 'id_shop' in request.POST:
            order.id_shop = get_object_or_404(Shop, idshop=request.POST['id_shop'])
        
        if 'payment_method' in request.POST:
            order.payment_method = request.POST['payment_method']

        order.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class ChangeOrderProduct(APIView):
    def put(self, request: Request):
        orderproduct = Orderproduct.objects.filter(Product.objects.get(idproduct=request.PUT['id_product'])).first()
        if orderproduct == None:
            return Response({'error' : 'Товар не найден!'}, status=status.HTTP_404_NOT_FOUND)
        
        orderproduct.amount_product -= request.PUT['amount_item']
        orderproduct.save()

        return Response(OrderproductSerializer(orderproduct).data)


    def delete(self, request: Request):
        order = get_object_or_404(Order, id_user=get_object_or_404(User, iduser=request.data['id_user']), status='Не оформлен') 
        orderproduct = Orderproduct.objects.filter(id_order=order, id_product=get_object_or_404(Product, idproduct=request.data['id_product'])).first()
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