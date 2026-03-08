from django.shortcuts import render
from order.serializer import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from order.models import Cart, CartItem
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from order.serializer import OrderSerializer, CreateOrderSerilaizer, UpdateOrderSerializer, CancelOrderSerializer
from order.models import Order
from rest_framework.decorators import action
from order.services import OrderService
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from sslcommerz_lib import SSLCOMMERZ


class CartViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        return Cart.objects.prefetch_related('items__product').filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        existing_cart = Cart.objects.filter(user=request.user).first()

        if existing_cart:
          serializer = self.get_serializer(existing_cart)
          return Response(serializer.data, status=status.HTTP_200_OK)

        return super.create(request, *args, **kwargs)


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs.get('cart_pk'))

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        else:
            return CartItemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):    # we can use this to without using get
            return context
        return {'cart_id':self.kwargs.get('cart_pk')}

class OrderViewSet(ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        OrderService.cancel_order(order=order, user=request.user)
        return Response({'Order Canceled'})

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = UpdateOrderSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({f'Order status updated to {request.data["status"]}'})


    def get_permissions(self):
        if self.action in ['update_status', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.prefetch_related('items__product').filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'cancel':
            return CancelOrderSerializer
        elif self.action == 'create':
            return CreateOrderSerilaizer
        elif self.action == 'partial_update':
            return UpdateOrderSerializer
        else:
            return OrderSerializer

    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context()
        return {
            'user_id':self.request.user.id,
            'user': self.request.user
        }


@api_view(['POST'])
def initiate_payment(request):
    user = request.user
    amount = request.data.get('amount')
    order_id = request.data.get('orderId')
    num_items = request.data.get('numItems')
    settings = {
        "store_id": "phima69ac8589a1fca",
        "store_pass": "phima69ac8589a1fca@ssl",
        "issandbox": True,
    }
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = f'tnx_{order_id}'
    post_body["success_url"] = "http://localhost:5173/dashboard/payment/success/"
    post_body["fail_url"] = "http://localhost:5173/dashboard/payment/fail/"
    post_body["cancel_url"] = "http://localhost:5173/dashboard/payment/cancel/"
    post_body['emi_option'] = 0
    post_body['cus_name'] = f'{user.first_name} {user.last_name}'
    post_body['cus_email'] = user.email
    post_body['cus_phone'] = user.phone_number
    post_body['cus_add1'] = user.address
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Ecommerce Products"
    post_body['product_category'] = "General"
    post_body['product_profile'] = "general"

    response = sslcz.createSession(post_body) # API response

    if response.get('status') == 'SUCCESS':
        return Response({"payment_page_url": response["GatewayPageURL"]})
    else:
        return Response({'Error': 'Payment Initiate Failed'})
