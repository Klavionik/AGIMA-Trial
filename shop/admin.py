from django.contrib import admin

from shop import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass


class CartItems(admin.TabularInline):
    model = models.CartItem

    def get_field_queryset(self, db, db_field, request):
        if db_field.name == 'product':
            return models.Product.objects.select_related('brand')


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}


@admin.register(models.Banner)
class BannerAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [
        CartItems
    ]
