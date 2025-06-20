from rest_framework import serializers
# from .models import *
from .models import *

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('idsection', 'name', 'path_image')

class CategorySerializer(serializers.ModelSerializer):
    id_section = SectionSerializer(read_only=True, source='section.name')
    
    class Meta:
        model = Category
        fields = ('idcategory', 'id_section', 'name', 'path_image')
        
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('idcolor', 'name')

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('id_user', 'id_product')

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ('idmanufacturer', 'name', 'country', 'rating_sum', 'rating_count')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('idorder', 'id_user', 'id_shop', 'payment_method', 'status', 'date_of_regestration')

class OrderproductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orderproduct
        fields = ('id_order', 'id_product', 'amount_product')

class ProcessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Processor
        fields = ('idprocessor', 'name')

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('idsubcategory', 'id_category', 'name', 'path_image')

class ProductSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Product
        fields = ('idproduct', 'id_property', 'id_subcategory', 'id_manufacturer', 'id_color', 'name', 'describe', 'price', 'amount', 'rating_count', 'rating_sum', 'status')

class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ('idproduct_photo', 'id_product', 'url_photo')

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('idproperty', 'id_type_display', 'id_video_card', 'id_processor', 'display_brightness_cd_m_2_field', 'maximum_screen_frequency_hz_field', 'screen_diagonal_inch_field', 'ram_amount_gb_field', 'internal_memory_amount_gb_field', 'thickness_mm_field', 'width_mm_field', 'height_mm_field', 'weight_kg_field')

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('idshop', 'addres', 'rating_sum', 'rating_count', 'contact_info')

class TypeDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeDisplay
        fields = ('idtype_display', 'name')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('iduser', 'status', 'position', 'lastname', 'firstname', 'midlename', 'birthdate', 'mail', 'password', 'phone_number')

class VideoCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoCard
        fields = ('idvideo_card', 'name')