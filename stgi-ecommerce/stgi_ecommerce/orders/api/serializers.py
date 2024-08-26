from rest_framework import serializers
from orders.models import Customer, Product, Order, OrderItem

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    # I wanted to use only product_id (Integer field rather than nestedSerializers) in API this seems to convenction 
    # but I think it creates an overhead. Please suggest in case
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all()) 

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']
        read_only_fields = ['price']

    def validate(self, data):
        product = data['product']
        data['price'] = product.price * data['quantity']
        return data


class OrderSerializer(serializers.ModelSerializer):
    # customer = CustomerSerializer()
    # I wanted to use only customer_id (Integer field rather than nestedSerializers) in API this seems to convenction 
    # but I think it creates an overhead. Please suggest in case
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    order_items = OrderItemSerializer(many=True)
    order_summary = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['customer', 'order_date', 'status', 'order_items', 'total_amount', 'order_summary']

    def get_order_summary(self, obj):
        return [
            {
                'product': item.product.name,
                'quantity': item.quantity,
                'price': item.product.price,
                'total': item.quantity * item.product.price
            }
            for item in obj.order_items.all()
        ]

    def validate(self, data):
        for item in data['order_items']:
            if item['quantity'] > item['product'].stock:
                raise serializers.ValidationError(f"Not enough stock for {item['product'].name}")
        return data
    
    # I'm doing this to create order and order items in the same go and adding total price to the order
    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')        
        order = Order.objects.create(**validated_data)
        total = 0        
        for item_data in order_items_data:
            product = item_data['product']
            item_data['price'] = product.price * item_data['quantity']
            total+= item_data['price']
            OrderItem.objects.create(order=order, **item_data)
        order.total_amount = total
        order.save()
        return order
