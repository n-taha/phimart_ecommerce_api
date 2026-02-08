from rest_framework import serializers
from order.models import Cart, CartItem
from product.serializer import ProductSerializer
from product.models import Product
from order.models import Order, OrderItem
from order.services import OrderService


# for get to show
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


# for post
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            self.instance = cart_item.save()
        except:
            self.instance = cart_item = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f'Product with this id {value} just not exist')
        return value

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class CartItemSerializer(serializers.ModelSerializer):
    # product_price = serializers.SerializerMethodField('get_product_price')
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField('get_total_price')
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, cart_item: CartItem):
        return cart_item.product.price * cart_item.quantity

    # def get_product_price(self, cart_item: CartItem):
    #     return cart_item.product.price

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField('get_total_price')
    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']
        read_only_fields = ['user']

    def get_total_price(self, cart:Cart):
        total_price_all = 0
        for i in cart.items.all():
            total_price_all += i.product.price * i.quantity
        return total_price_all

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'total_price']

class CreateOrderSerilaizer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('Cart is not found')
        elif not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('This cart is empty')
        else:
            return cart_id

    def create(self, validated_data):
        cart_id = validated_data['cart_id']
        user_id = self.context['user_id']

        try:
            order = OrderService.create_order(cart_id=cart_id, user_id=user_id)
            return order
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def to_representation(self, instance):
        return OrderSerializer(instance).data


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['user', 'status', 'total_price', 'created_at', 'items']

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

        # if we use action decorator we no need to override update method.

"""    def update(self, instance, validated_data):
        user = self.context['user']
        status = validated_data['status']

        if status == Order.CANCELED:
            return OrderService.cancel_order(order=instance, user=user)

        if not user.is_staff:
            raise serializers.ValidationError({
                'details':'You are not allowed to update the order status'
            })

        instance.status = status
        instance.save()
        return instance"""

class CancelOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = []


# class OrderItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields =