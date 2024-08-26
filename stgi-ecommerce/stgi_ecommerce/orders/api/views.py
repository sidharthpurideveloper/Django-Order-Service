from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from orders.models import Customer, Product, Order, OrderItem
from .serializers import CustomerSerializer, ProductSerializer, OrderSerializer
from .filters import OrderFilter 


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related('customer').prefetch_related('order_items__product').order_by('-order_date')
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'order_date', 'customer']
    filterset_class = OrderFilter

    @action(detail=True, methods=['post'])
    def mark_as_shipped(self, request, pk=None):
        order = self.get_object()
        order.status = Order.SHIPPED
        order.save()
        return Response({'status': 'Order marked as shipped'}, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = super().get_queryset()        
        customer_email = self.request.query_params.get('customer_email', None)
        customer_id = self.request.query_params.get('customer_id', None)        
        if customer_email:
            queryset = queryset.filter(customer__email=customer_email)        
        if customer_id:
            queryset = queryset.filter(customer__id=customer_id)
        return queryset
    
    # I'm decreasing the quantity of each product in the order
    def perform_create(self, serializer):
        order = serializer.save()
        for item in order.order_items.all():
            product = item.product
            product.stock -= item.quantity
            if product.stock < 0:
                product.stock = 0 
            product.save()

