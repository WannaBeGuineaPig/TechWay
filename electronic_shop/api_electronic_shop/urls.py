from django.urls import path, include
from . import views

urlpatterns = [
    path('user_list/', views.UserList.as_view()),
    path('auth_reg_user/', views.AuthorizationRegistrationUser.as_view()),
    path('auth_reg_user/<int:pk>', views.AuthorizationRegistrationUser.as_view()),
    path('product_list/', views.ProductList.as_view()),
    path('add_to_basket/', views.AddToBasket.as_view()),
    path('basket_list/', views.BasketList.as_view()),
    path('shop_list/', views.ShopList.as_view()),
    path('update_data_order/', views.UpdateDataOrder.as_view()),
    path('change_order_product/', views.ChangeOrderProduct.as_view()),
    path('get_product/<int:id_product>', views.GetProduct.as_view()),
    path('', include('rest_framework.urls', namespace='rest_framework'))
]



# Попробывовать переделать на роутер!

# from django.urls import path, include
# from rest_framework import routers
# from . import views

# router = routers.DefaultRouter()

# lst_api = [
#     ['user_list/', views.UserList.as_view()],
#     ['auth_reg_user/', views.AuthorizationRegistrationUser.as_view()],
#     # ['auth_reg_user/<int:pk>', views.AuthorizationRegistrationUser.as_view()],
#     ['product_list/', views.ProductList.as_view()]
# ]

# for i in range(len(lst_api)):
#     router.register(lst_api[i][0], lst_api[i][1])


# urlpatterns = [
#     # path('user_list/', views.UserList.as_view()),
#     # path('auth_reg_user/', views.AuthorizationRegistrationUser.as_view()),
#     # path('auth_reg_user/<int:pk>', views.AuthorizationRegistrationUser.as_view()),
#     # path('product_list/', views.ProductList.as_view()),
#     path('', include(router.urls)),
#     path('', include('rest_framework.urls', namespace='rest_framework'))
# ]