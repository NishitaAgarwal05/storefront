
from django.db.models import DecimalField
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q, F
from django.core.exceptions import ObjectDoesNotExist
from store.models import Collection, Product, Order, OrderItem, Customer
from django.db.models.aggregates import Count, Min, Max, Aggregate
from django.db.models import Value, Func, ExpressionWrapper
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType
from store.models import Product
from tags.models import TaggedItem
from django.db import transaction
from django.db import connection

# Create your views here.
def say_hello(request):
    # return HttpResponse('Hello World')
    # query_set = Product.objects.filter(Q(inventory__lt=10)|Q(unit_price__lt=20))
    #earliest= sort in asc order and get the first element, latest = descending order nd gpet first element
    # query_set = Product.objects.filter(inventory=F('collection__id')).order_by('unit_price','-title')[5:10]
    # query_set = Product.objects.values_list('id','title','collection__title')
    # query_set = Product.objects.filter(id__in = OrderItem.objects.values_list('product__id')).order_by('title').distinct()
    # select_related(1) - other side of instance has 1 instance
    # prefetch_related(n) - other side of instance has n instances
    # query_set = Product.objects.prefetch_related('promotions').all() # join between the tables
    # query_set = Product.objects.prefetch_related('promotions').select_related('collection').all()
    # query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    # return render(request, 'hello.html', {'orders':list(query_set)})


#Summarizing tables
    # result = Product.objects.aggregate(count = Count('id'))
    # return render(request, 'hello.html',{'result':result})


#Annotating objects
    # query_Set = Customer.objects.annotate(full_name = Concat('first_name', Value(" "),'last_name'))
    # query_Set = Customer.objects.annotate(orders_count = Count('order'))
    # discounted_price = ExpressionWrapper(F('unit_price')*0.8, output_field=DecimalField())
    # query_Set = Product.objects.annotate(
    #     discounted_price =  discounted_price
    # )
    # query_set = TaggedItem.objects.get_tags_for(Product,1)

#Saving objects in database
    
    #Update
    # collection = Collection.objects.get(pk=1)
    # collection.featured_product = None
    # collection.save()
    # collection.id

    #Create
    # collection = Collection.objects.create(title='a', featured_product_id = 1)
    # collection.id

    #Delete
    # collection = Collection(pk=1)
    # collection.delete()

    #Delete multiple objects
    # Collection.objects.filter(id__gt=5).delete()

#Transactions
    # with transaction.atomic():
    #     order = Order.objects.create(
    #         id = 1002,
    #         customer_id = 1
    #     )

    #     item = OrderItem()
    #     item.id = 1002
    #     item.order = order
    #     item.product_id =-1
    #     item.quantity = 1
    #     item.unit_price = 10
    #     item.save()

#Executing raw queries
    # querySet = Product.objects.raw('SELECT id, title from store_product')

    # cursor = connection.cursor()
    # cursor.execute()

    with connection.cursor() as cursor:
        cursor.execute()
        # executing stored procedure
        cursor.callproc('get_customers',[1,2,'a'])


    return render(request,'hello.html',{'result':list(querySet)})