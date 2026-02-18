from django.urls import path
from .views import AllOrders, AllUserView, Create_payment, DashboardRevenueView,EditUserView, ProductsingleView, UpdateOrderStatusView,UserView,AllProducts,soft_delete_view,EditProductView,AddproductView
urlpatterns = [
    path('usermanage/',AllUserView.as_view(),name='usermanage'),
    path('userEdit/<int:pk>/',EditUserView.as_view(),name='useredit'),
    path('userView/<int:pk>/',UserView.as_view(),name='user'),
    ##
    path('productView/',AllProducts.as_view(),name='allproducts'),
    path('productsDelete/<int:pk>/',soft_delete_view,name='delete_product'),
    path('productsEdit/<int:pk>/',EditProductView.as_view(),name='editproduct'),
    path('productsingleView/<int:pk>/',ProductsingleView.as_view(),name='product'),
    path('productsadd/',AddproductView.as_view(),name='addproduct'),
    path('create_payment/',Create_payment,name='create_payment' \
    ''),
    path('orders/users/',AllOrders.as_view(),name='allorders'),
    path('dashboard/', DashboardRevenueView.as_view(), name='dashboard'),
    path('orders/update/<int:pk>/', UpdateOrderStatusView.as_view(), name='update-order')
]
