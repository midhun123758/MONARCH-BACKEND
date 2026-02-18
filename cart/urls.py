from django.urls import path
from .views import Addtocart, UserCartview,UpdateCart,DeleteCart

urlpatterns = [
    path('add/', Addtocart.as_view(), name='add-to-cart'),
    path('view/', UserCartview.as_view(), name='user-cart'),
    path('update/<int:item_id>/',UpdateCart.as_view(),name='user_update'),
    path('delete/<int:item_id>/',DeleteCart.as_view(),name='delete')
]
