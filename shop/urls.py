from django.urls import path
from .views import *



urlpatterns = [
    path('',Product_ListView.as_view(),name="home"),
    path('product/<int:pk>/',Product_DetailView.as_view(),name="product_detail"),
    path('product/add/',Product_CreateView.as_view(),name="product_add"),
    path('product/<int:pk>/edit/',Product_UpdateView.as_view(),name="product_edit"),
    path('product/<int:pk>/delete/',Product_DeleteView.as_view(),name="product_delete"),
    path('cart/',CartItemListView.as_view(),name="cart_items"),
    path('cart/add/<int:pk>/',AddToCartView.as_view(),name="add_to_cart"),
    path('cart/remove/<int:pk>/',RemoveFromCartView.as_view(),name="remove_from_cart"),
    path('order/place/',PlaceOrderView.as_view(),name="place_order"),
    path('login/',UserLoginView.as_view(),name="login"),
    path('logout/',UserLogoutView.as_view(),name="logout"),
    path('register/',Register.as_view(),name="register"),
    path('orders/',OrderListView.as_view(),name="order_list"),
    
]