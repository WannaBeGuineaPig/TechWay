from django.urls import path
from . import views

app_name = 'TechWay'
urlpatterns = [
    path('home', views.main_window, name='home'),
    path('catalog', views.catalog_window, name='catalog'),
    path('favorite', views.favorite_window, name='favorite'),
    path('backet', views.backet_window, name='backet'),
    path('personal_account', views.personal_account_window, name='personal_account')
]
