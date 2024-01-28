from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http.request import HttpRequest

from tags.models import Tag, TaggedItem
from . import models
from django.utils.html import format_html,urlencode
from django.db.models import Count
from django.urls import reverse
# Register your models here.

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ('<10','Low')
        ]
    
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any]:
        if self.value() =='<10':
            return queryset.filter(inventory__lt=10)

    
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # fields = ['title', 'slug']
    # exclude=['promotions']
    # readonly_fields = ['title']
    prepopulated_fields = {
        'slug': ['title']
        }
    search_fields = ['title']
    autocomplete_fields = ['collection']
    actions = ['clear_inventory']
    list_display = ['title','unit_price', 'inventory_status','collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter]

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory<10:
            return 'LOW'
        return 'OK'
    
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated',
            messages.ERROR
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership', 'orders_count']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name','user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        #reverse('admin:app_model_page')
        url = ( 
                reverse('admin:store_order_changelist') 
                + '?'
                + urlencode({
                    'customer__id': str(customer.id) 
                })
            )
        return  format_html('<a href="{}">{}</a>',url, customer.orders_count)
        
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            orders_count = Count('order')
        )
    
class OrderItemInline(admin.StackedInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    extra = 0
    min_num = 1
    max_num = 10
    

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','placed_at','customer']
    inlines=[OrderItemInline]
    autocomplete_fields = ['customer']

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self,collection):
        #reverse('admin:app_model_page')
        url = ( 
                reverse('admin:store_product_changelist') 
                + '?'
                + urlencode({
                    'collection__id': str(collection.id) 
                })
            )
        return  format_html('<a href="{}">{}</a>',url, collection.products_count)
        
    
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            products_count = Count('products')
        )
    
