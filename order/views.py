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

class CartViewSet(GenericViewSet, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        return Cart.objects.prefetch_related('items__product').filter(user=self.request.user)


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