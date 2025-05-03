from django.urls import path
from . import views

urlpatterns = [
    path('user_list/', views.UserList.as_view()),
    path('auth_reg_user/', views.AuthorizationRegistrationUser.as_view()),
    path('auth_reg_user/<int:pk>', views.AuthorizationRegistrationUser.as_view()),
    path('product_list/', views.ProductList.as_view()),
    # path('manufacturers/', views.ManufacturerList.as_view()),
    # path('manufacturers/<int:pk>', views.ManufacturerDetail.as_view())
]