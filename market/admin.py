from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import Product,Shop,Image,Category,Order,OrderProduct
from django.utils.html import format_html
from django.db.models import Count



class PriceRangeFilter(admin.SimpleListFilter):
    title = 'Price Range'
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return (
            ('0_100', '0 - 100'),
            ('101_200', '101 - 200'),
            ('201_300', '201 - 300'),
       
        )

    def queryset(self, request, queryset):
        if self.value():
            min_price, max_price = self.value().split('_')
            return queryset.filter(price__gte=min_price, price__lte=max_price)


class ShopAdmin(admin.ModelAdmin):
    list_display=[
        "title",
        "description",
        'image_tag'
    ]
    search_fields=[
        "title"
    ]
    def image_tag(self,obj):
        if obj.image_url:
            return format_html('<img src="%s" style="max-width:100px; max-height:100px;" />' % obj.image_url.url)
        else:
            return 'No Image'
        
    image_tag.allow_tags = True
    list_per_page=3 #navigate through pages of shop lists


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'amount', 'price', 'active', 'shop', 'num_orders', 'price_sort','get_image']
    search_fields = ['id','title']
    readonly_fields = ['get_image']
    list_filter=['active',PriceRangeFilter]
    list_per_page=3
    #navigate through pages of shop lists

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        queryset=super().get_queryset(request)
        queryset=queryset.annotate(num_orders=Count('orderproduct'))
        return queryset
    
    # def get_ordering(self, request):
    #     # Sort by number of orders in descending order
    #     return ['-num_orders']

    def get_image(self,obj):
        first_image=obj.image_set.first()
        if first_image:
            return format_html('<img src="%s" style="max-width:100px; max-height:100px;" />' % first_image.file.url)
        else:
            return 'No Image'
    get_image.short_description='Main image'
    

    def price_sort(self, obj):
        
        return obj.price

    price_sort.short_description = 'Price'
    price_sort.admin_order_field = 'price'

    def num_orders(self, obj):
        return obj.orderproduct_set.count()

    num_orders.short_description = 'Number of Orders'
    num_orders.admin_order_field = 'num_orders'
    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'parent','all_paths']
    search_fields = ['id', 'title', 'parent__title']
    list_filter = ['parent']
    list_per_page=3

    def all_paths(self, obj):#Display all possible paths to chosen category.
        paths = []
        category = obj
        while category.parent:
            paths.append(category.parent.title)
            category = category.parent
        return ' -> '.join(reversed(paths)) if paths else '-'
    all_paths.short_description = 'All Paths'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Shop,ShopAdmin)
admin.site.register(Image)
admin.site.register(Order)
admin.site.register(OrderProduct)