from django.urls import path
from . import views

app_name = 'TechWay'
urlpatterns = [
    path('home/', views.main_view, name='home'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('favorite/', views.favorite_view, name='favorite'),
    path('backet/', views.backet_view, name='backet'),
    path('personal_account/', views.personal_account_view, name='personal_account'),
    path('authorization/', views.authorization_view, name='auth'),
    path('registration/', views.registration_view, name='reg'),
    path('product/<int:product_id>', views.product_view, name='product_window'),
    path('admin_panel/', views.admin_panel_view, name='admin_panel'),
    path('personal_account_admin/', views.personal_account_admin_view, name='personal_account_admin'),
    path('update_list_product/', views.update_product_list),
    path('add_to_basket/<int:product_id>', views.add_to_basket),
    path('delete_item_basket/', views.delete_item_basket),
    path('change_data_basket/', views.change_data_basket),
    path('get_list_data_admin/', views.get_list_data_admin),
    path('update_status_order/', views.update_status_order),
    path('create_report_admin_panel/', views.create_report_admin_panel),
    path('delete_admin_panel/', views.delete_admin_panel),
    path('add_change_data/', views.add_change_data),
    path('add_change_data_page/', views.add_change_data_view, name='add_change'),
    path('history_order/', views.history_order_view, name='history_order'),
    path('create_check_history_order/', views.create_check_history_order),
    path('add_favorite_item/', views.add_favorite_item),
    path('delete_favorite_item/', views.delete_favorite_item),
    path('password_recovery/', views.password_recovery_view, name='password_recovery'),
    path('change_password/<str:hash>/', views.change_password_view, name='change_password'),
]
