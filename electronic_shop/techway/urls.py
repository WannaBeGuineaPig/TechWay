from django.urls import path
from . import views

app_name = 'TechWay'
urlpatterns = [
    path('home/', views.main_window, name='home'),
    path('catalog/', views.catalog_window, name='catalog'),
    path('favorite/', views.favorite_window, name='favorite'),
    path('backet/', views.backet_window, name='backet'),
    path('personal_account/', views.personal_account_window, name='personal_account'),
    path('authorization/', views.authorization_window, name='auth'),
    path('registration/', views.registration_window, name='reg'),
    path('product/<int:product_id>', views.product_window),
    path('update_list_product/', views.update_product_list)
]
