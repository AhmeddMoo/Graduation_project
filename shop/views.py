from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Product, CartItem, Order
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy


class Product_ListView(ListView):
    model = Product
    template_name = "shop/home.html"
    context_object_name = "products"


class Product_DetailView(DetailView):
    model = Product
    template_name = "shop/detail.html"
    context_object_name = "Details_product"


class Product_DeleteView(DeleteView,UserPassesTestMixin):
    model = Product
    template_name = "shop/product_confirm_delete.html"
    success_url = reverse_lazy("home")
    def test_func(self):
        product = self.get_object()
        return self.request.user == product.user


class Product_CreateView(LoginRequiredMixin,CreateView):
    model = Product
    template_name = "shop/product_form.html"
    fields = ["name", "description", "price", "stock", "image"]
    success_url = reverse_lazy("home")
    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)


class Product_UpdateView(UpdateView,UserPassesTestMixin):
    model = Product
    template_name = "shop/product_form.html"
    fields = ["name", "description", "price", "stock", "image"]
    success_url = reverse_lazy("home")
    def test_func(self):
        product = self.get_object()
        return self.request.user == product.user


class CartItemListView(LoginRequiredMixin,ListView):
    model = CartItem
    template_name = "shop/cart.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        cart_items = CartItem.objects.filter(user=self.request.user)

        return cart_items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_price"] = sum(
            item.product.price * item.quantity for item in context["cart_items"]
        )
        return context


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, product=product
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        return redirect("cart_items")


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk, user=request.user)
        cart_item.delete()
        return redirect("cart_items")


class PlaceOrderView(LoginRequiredMixin, View):
    def post(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return redirect("cart_items")
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        order = Order.objects.create(user=request.user, total_price=total_price)
        for item in cart_items:
            if item.product.stock>=item.quantity:
                item.product.stock-=item.quantity
                item.product.save()

            else:
                HttpResponse("Out of stock")
        cart_items.delete()
        return render(request, "shop/order_success.html", {"order": order})


class OrderListView(LoginRequiredMixin,ListView):
    model = Order
    template_name = "shop/order_list.html"
    context_object_name = "orders"


class UserLoginView(LoginView):
    template_name = "shop/login.html"

    def get_success_url(self):

        return reverse_lazy("home")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")


class Register(CreateView):
    def get(self, request):
        return render(request, "shop/register.html")

    def post(self, request):
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 != password2:
            return HttpResponse("Password do not match")
     
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists")

       
        User.objects.create_user(username=username, password=password1)
        return redirect("login")

# Create your views here.
