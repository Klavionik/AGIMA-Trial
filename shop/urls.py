from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from shop.views import SignUpView, ProductDetailView, AddProductToCartView, CartView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('catalog/<slug:product>/', ProductDetailView.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', AddProductToCartView.as_view(), name='add-product')
]
