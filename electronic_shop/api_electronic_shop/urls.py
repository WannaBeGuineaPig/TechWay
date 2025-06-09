from django.urls import path, include
from . import views

urlpatterns = [
    path('user_list/', views.UserList.as_view()),
    path('shop_list/', views.ShopList.as_view()),
    path('order_list/', views.OrderList.as_view()),
    path('subcategory_list/', views.SubcategoryList.as_view()),
    path('section_list/', views.SectionList.as_view()),
    path('manufacturer_list/', views.ManufacturerList.as_view()),
    path('color_list/', views.ColorList.as_view()),
    path('type_display_list/', views.TypeDisplayList.as_view()),
    path('video_card_list/', views.VideoCardList.as_view()),
    path('processor_list/', views.ProcessorList.as_view()),
    path('auth_reg_user/', views.AuthorizationRegistrationUser.as_view()),
    path('auth_reg_user/<int:pk>', views.AuthorizationRegistrationUser.as_view()),
    path('product_list/', views.ProductList.as_view()),
    path('add_to_basket/', views.AddToBasket.as_view()),
    path('basket_list/', views.BasketList.as_view()),
    path('update_data_order/', views.UpdateDataOrder.as_view()),
    path('change_order_product/', views.ChangeOrderProduct.as_view()),
    path('get_product/<int:id_product>', views.GetProduct.as_view()),
    path('receive_cleared_products/', views.ReceiveClearedProducts.as_view()),
    path('product_list_admin_panel/', views.ProductListAdminPanel.as_view()),
    path('order_list_admin_panel/', views.OrderListAdminPanel.as_view()),
    path('employee_list_admin_panel/', views.EmployeeListAdminPanel.as_view()),
    path('update_status_order_admin_panel/', views.UpdateStatusOrderAdminPanel.as_view()),
    path('list_for_report_admin_panel/', views.ListForReportAdminPanel.as_view()),
    path('update_status_item_admin_panel/', views.UpdateStatusItemAdminPanel.as_view()),
    path('update_status_employee_admin_panel/', views.UpdateStatusEmployeeAdminPanel.as_view()),
    path('get_set_data_product/', views.GetSetDataProduct.as_view()),
    path('get_set_data_employee/', views.GetSetDataEmployee.as_view()),
    path('history_order_user/', views.HistoryOrderUser.as_view()),
    path('order_product_for_check/', views.OrderProductForCheck.as_view()),
    path('category_list_catalog/', views.CategoryListCatalog.as_view()),
    path('subcategory_list_catalog/', views.SubcategoryListCatalog.as_view()),
    path('categoty_section/', views.CategotySection.as_view()),
    path('favorite_action/', views.FavoriteAction.as_view()),
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