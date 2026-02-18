from django.urls import path
from .views import AddToWishlist,UserWishlistView,DeleteWishlistItem
urlpatterns = [
    path('wishlist_add/',AddToWishlist.as_view(),name='add_wishlist'),
    path ('wishlist_View/',UserWishlistView.as_view(),name='view_wishlist'),
     path('delete/<int:item_id>/',DeleteWishlistItem.as_view(),name='delete')
]
