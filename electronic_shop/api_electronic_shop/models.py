# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Category(models.Model):
    idcategory = models.IntegerField(primary_key=True)
    id_section = models.ForeignKey('Section', models.DO_NOTHING, db_column='id_section')
    name = models.CharField(max_length=45)
    path_image = models.TextField()

    class Meta:
        managed = False
        db_table = 'category'


class Color(models.Model):
    idcolor = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'color'


class Favorite(models.Model):
    pk = models.CompositePrimaryKey('id_product', 'id_user')
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user')
    id_product = models.ForeignKey('Product', models.DO_NOTHING, db_column='id_product')

    class Meta:
        managed = False
        db_table = 'favorite'
        unique_together = (('id_product', 'id_user'),)


class Manufacturer(models.Model):
    idmanufacturer = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    country = models.CharField(max_length=45)
    rating_sum = models.FloatField()
    rating_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'manufacturer'


class Order(models.Model):
    idorder = models.AutoField(primary_key=True)
    id_user = models.ForeignKey('User', models.DO_NOTHING, db_column='id_user')
    id_shop = models.ForeignKey('Shop', models.DO_NOTHING, db_column='id_shop', blank=True, null=True)
    payment_method = models.CharField(max_length=9, blank=True, null=True)
    status = models.CharField(max_length=15)
    date_of_regestration = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order'


class Orderproduct(models.Model):
    pk = models.CompositePrimaryKey('id_order', 'id_product')
    id_order = models.ForeignKey(Order, models.DO_NOTHING, db_column='id_order')
    id_product = models.ForeignKey('Product', models.DO_NOTHING, db_column='id_product')
    amount_product = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'orderproduct'
        unique_together = (('id_order', 'id_product'),)


class Processor(models.Model):
    idprocessor = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'processor'


class Product(models.Model):
    idproduct = models.AutoField(primary_key=True)
    id_property = models.ForeignKey('Property', models.DO_NOTHING, db_column='id_property')
    id_subcategory = models.ForeignKey('Subcategory', models.DO_NOTHING, db_column='id_subcategory')
    id_manufacturer = models.ForeignKey(Manufacturer, models.DO_NOTHING, db_column='id_manufacturer')
    id_color = models.ForeignKey(Color, models.DO_NOTHING, db_column='id_color')
    name = models.CharField(max_length=100)
    describe = models.TextField()
    price = models.FloatField()
    amount = models.IntegerField()
    rating_count = models.FloatField()
    rating_sum = models.FloatField()
    status = models.CharField(max_length=14)

    class Meta:
        managed = False
        db_table = 'product'


class ProductPhoto(models.Model):
    idproduct_photo = models.AutoField(primary_key=True)
    id_product = models.ForeignKey(Product, models.DO_NOTHING, db_column='id_product')
    url_photo = models.TextField()

    class Meta:
        managed = False
        db_table = 'product_photo'


class Property(models.Model):
    idproperty = models.AutoField(primary_key=True)
    id_type_display = models.ForeignKey('TypeDisplay', models.DO_NOTHING, db_column='id_type_display', blank=True, null=True)
    id_video_card = models.ForeignKey('VideoCard', models.DO_NOTHING, db_column='id_video_card', blank=True, null=True)
    id_processor = models.ForeignKey(Processor, models.DO_NOTHING, db_column='id_processor', blank=True, null=True)
    display_brightness_cd_m_2_field = models.IntegerField(db_column='display_brightness(cd/m^2)', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    maximum_screen_frequency_hz_field = models.IntegerField(db_column='maximum_screen_frequency(Hz)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    screen_diagonal_inch_field = models.FloatField(db_column='screen_diagonal(inch)', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    ram_amount_gb_field = models.FloatField(db_column='RAM_amount(Gb)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    internal_memory_amount_gb_field = models.FloatField(db_column='internal_memory_amount(Gb)', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    thickness_mm_field = models.FloatField(db_column='thickness(mm)', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    width_mm_field = models.FloatField(db_column='width(mm)', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    height_mm_field = models.FloatField(db_column='height(mm)', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    weight_kg_field = models.FloatField(db_column='weight(kg)', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'property'


class Section(models.Model):
    idsection = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    path_image = models.TextField()

    class Meta:
        managed = False
        db_table = 'section'


class Shop(models.Model):
    idshop = models.AutoField(primary_key=True)
    addres = models.TextField()
    rating_sum = models.FloatField()
    rating_count = models.IntegerField()
    contact_info = models.TextField()

    class Meta:
        managed = False
        db_table = 'shop'


class Subcategory(models.Model):
    idsubcategory = models.AutoField(primary_key=True)
    id_category = models.ForeignKey(Category, models.DO_NOTHING, db_column='id_category')
    name = models.CharField(max_length=45)
    path_image = models.TextField()

    class Meta:
        managed = False
        db_table = 'subcategory'


class TypeDisplay(models.Model):
    idtype_display = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'type_display'


class User(models.Model):
    iduser = models.AutoField(primary_key=True)
    status = models.CharField(max_length=7)
    position = models.CharField(max_length=23)
    lastname = models.CharField(max_length=45)
    firstname = models.CharField(max_length=45)
    midlename = models.CharField(max_length=45, blank=True, null=True)
    birthdate = models.DateTimeField()
    mail = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'user'


class VideoCard(models.Model):
    idvideo_card = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'video_card'
