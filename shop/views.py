from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView

from shop.forms import SignupForm
from shop.models import Product, Cart, Banner


class AddProductToCartView(View):
    success_message = 'Добавлено!'
    failure_message = 'Ошибка, попробуйте еще раз.'

    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponse(status=405)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.update_cart()
        return JsonResponse({'message': self.success_message})

    def update_cart(self):
        pk = self.kwargs.get('product_id')
        product = self.get_product(pk)
        cart_item, created = self.request.user.cart.items.get_or_create(
            cart__customer=self.request.user,
            product=product
        )
        if not created:
            cart_item.add()

    def get_product(self, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return JsonResponse({'message': self.failure_message})
        else:
            return product


class CartView(View):
    template_name = 'shop/cart.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('clear'):
            return self.clean_cart()
        ctx = self.get_context()
        return render(request, 'shop/cart.html', context=ctx)

    def clean_cart(self):
        cart = Cart.objects.get(customer=self.request.user)
        cart.items.all().delete()
        return redirect('cart')

    def get_cart(self):
        if self.request.user.is_authenticated:
            return Cart.objects.get(customer=self.request.user)
        return None

    def get_context(self):
        cart = self.get_cart()

        if cart is not None:
            items = cart.items.all()
        else:
            items = []

        context = {'cart': cart, 'items': items}
        return context


class SignUpView(CreateView):
    template_name = "shop/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        message = 'Успешная регистрация! Теперь вы можете войти.'
        messages.success(self.request, message)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ProductDetailView(DetailView):
    template_name = 'shop/product.html'
    model = Product
    slug_url_kwarg = 'product'
    context_object_name = 'product'


class HomeView(ListView):
    template_name = 'shop/home.html'
    model = Banner
    context_object_name = 'banners'
