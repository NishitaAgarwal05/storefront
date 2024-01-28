from rest_framework import serializers
from .models import Product, Collection, Reviews, Cart,CartItem, Customer, Order, OrderItem
from decimal import Decimal

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model= Collection
        fields = ['id', 'title', 'product_count']

    product_count = serializers.IntegerField(read_only = True)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # # collection = CollectionSerializer()
    # # collection = serializers.PrimaryKeyRelatedField(pk=id)
    # # collection = serializers.StringRelatedField()
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name='collection-detail'
    # )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    
    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Passwords do not match')
    #     return data

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['id', 'name', 'description', 'date']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Reviews.objects.create(product_id=product_id, **validated_data)

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']

class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField(method_name='calculate_price')
    product= SimpleProductSerializer() 
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def calculate_price(self, cart_item:CartItem):
        return cart_item.quantity*cart_item.product.unit_price
    
class CartSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='calculate_price')
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
    
    def calculate_price(self, cart:Cart):
        total_price = Decimal(0.0)
        for items in cart.items.all():
            total_price = Decimal(total_price)+(Decimal(items.quantity)*Decimal(items.product.unit_price))
        return total_price

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

    def validate_product_id(self, value):
        if not Product.objects.filter(pk = value):
            raise serializers.ValidationError("No product with given id found")
        return value
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id = cart_id, product_id = product_id)
            cart_item.quantity = quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance



class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'quantity']
        
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        quantity = self.validated_data['quantity']
        cart_item = CartItem.objects.get(cart_id = cart_id)
        cart_item.quantity = quantity
        cart_item.save()
        self.instance = cart_item
        return self.instance
    
class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']

class OrderItemSerializer(serializers.ModelSerializer):
    product= SimpleProductSerializer() 
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'payment_status', 'customer', 'placed_at', 'items']




