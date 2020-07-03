from .models import Brand


def navbar(httprequest):
    brands = Brand.objects.order_by('title').prefetch_related('products')
    return {'brands': brands}
