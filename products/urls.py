from django.urls import path
from .views import ProductFilterView, ProductListViewI, ProductDetailView, Categerory_view
from . import views

urlpatterns = [
    path('', ProductListViewI.as_view(), name='product-list'),  # list all products
    path('details/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),  # single product
    path('ctg_view/<int:pk>/', Categerory_view.as_view(), name='category-products'),  # products by category
    path('create/', views.product_create, name='product-create'),  # create product
    path("filter/", ProductFilterView.as_view(), name="product-filter"),
]
