from rest_framework import serializers

from .order_item import OrderItemCreateSerializer, OrderItemListSerializer
from ..models import Order, OrderItem


class OrderCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    order_items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'city', 'address', 'phone_number', 'order_items']

    def create(self, validated_data):
        items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        user = order.user
        total_price = 0
        free_case_count = 0

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            price = product.price * quantity

            is_free = False

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price if not is_free else 0,  # Бесплатный товар будет стоить 0
                is_free=is_free
            )
            total_price += price if not is_free else 0  # Не добавляем цену бесплатных товаров в общую стоимость

        welcome_discount = user.welcome_discount or 0
        welcome_discount_amount = round((total_price * welcome_discount) / 100)
        total_price -= welcome_discount_amount

        # Birthday скидка
        birthday_discount = user.get_birthday_discount() or 0
        birthday_discount_amount = round((total_price * birthday_discount) / 100)
        total_price -= birthday_discount_amount

        order.total_price = round(total_price)
        order.discount = welcome_discount_amount + birthday_discount_amount
        order.welcome_discount = welcome_discount
        order.save()

        return order


class OrderListSerializer(serializers.ModelSerializer):
    order_items = OrderItemListSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'total_price', 'discount', 'status', 'order_items', 'created_at', 'updated_at']
