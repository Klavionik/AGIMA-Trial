from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Sum, F
from django.shortcuts import reverse


class User(AbstractUser):

    def __str__(self):
        return f"{self.username} {'Менеджер' if self.is_staff else 'Клиент'}"

    class Meta:
        db_table = 'users'
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Brand(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='название бренда'
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'brands'
        verbose_name = 'бренд'
        verbose_name_plural = 'бренды'


class Product(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='название товара'
    )
    slug = models.SlugField(
        max_length=100,
        verbose_name='ссылка',
    )
    description = models.TextField(
        max_length=1000,
        verbose_name='описание товара'
    )
    price = models.IntegerField(
        verbose_name='цена товара'
    )
    image = models.ImageField(
        upload_to='product_images',
        verbose_name='изображение'
    )
    brand = models.ForeignKey(
        'Brand',
        on_delete=models.CASCADE,
        verbose_name='бренд товара',
        related_name='products',
        related_query_name='product',
    )

    def __str__(self):
        return f'{self.title} {self.brand.title} {self.price}'

    def get_absolute_url(self):
        return reverse('product', args=[self.slug])

    class Meta:
        db_table = 'products'
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class Cart(models.Model):
    customer = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        unique=True,
    )

    def __str__(self):
        return f'корзина {self.customer}'

    def subtotal(self):
        return self.items.aggregate(subtotal=Sum(F('qty') * F('product__price')))['subtotal']

    def number_of_items(self):
        return self.items.aggregate(cart_qty=Sum('qty'))['cart_qty']

    class Meta:
        db_table = 'carts'
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.SET_NULL,
        related_name='+',
        null=True,
    )
    qty = models.PositiveIntegerField(
        default=1,
    )

    def __str__(self):
        return f'{self.product.title} в карте'

    def add(self):
        self.qty = F('qty') + 1
        self.save()

    def total_price(self):
        return self.qty * self.product.price

    class Meta:
        db_table = 'cart_items'
        verbose_name = 'товар в корзине'
        verbose_name_plural = 'товары в корзине'


class Banner(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name='название баннера'
    )
    image = models.ImageField(
        verbose_name='изображение баннера',
        upload_to='banners',
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        db_table = 'banners'
        verbose_name = 'баннер'
        verbose_name_plural = 'баннеры'
