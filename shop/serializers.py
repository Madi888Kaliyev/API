# shop/serializers.py
from decimal import Decimal
from django.core.mail import send_mail
from rest_framework import serializers

from .models import Furniture, Order, OrderItem


# ---------- Furniture ----------
class FurnitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Furniture
        fields = ["id", "name", "price", "category"]


# ---------- READ: Orders (GET) ----------
class OrderItemReadSerializer(serializers.ModelSerializer):
    furniture = FurnitureSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "furniture", "price", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemReadSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "email", "total_amount", "created_at", "items"]


# ---------- CREATE: Orders (POST) ----------
class OrderItemInputSerializer(serializers.Serializer):
    # Принимаем ID, но валидатор вернёт УЖЕ объект Furniture
    furniture = serializers.PrimaryKeyRelatedField(queryset=Furniture.objects.all())
    quantity = serializers.IntegerField(min_value=1, default=1)


class CreateOrderSerializer(serializers.Serializer):
    email = serializers.EmailField()
    items = OrderItemInputSerializer(many=True)

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        email = validated_data["email"]

        order = Order.objects.create(email=email, total_amount=Decimal("0"))
        total = Decimal("0")
        to_create: list[OrderItem] = []

        for item in items_data:
            furn: Furniture = item["furniture"]    # ← это уже объект, НЕ id
            qty: int = item.get("quantity", 1)
            price = furn.price                      # Decimal
            to_create.append(
                OrderItem(order=order, furniture=furn, price=price, quantity=qty)
            )
            total += price * qty

        OrderItem.objects.bulk_create(to_create)
        order.total_amount = total
        order.save(update_fields=["total_amount"])

        # Письмо клиенту (MailHog перехватит, если он подключён)
        try:
            lines = [f"{oi.furniture.name} — {oi.price} × {oi.quantity}" for oi in to_create]
            body = "Ваш заказ создан:\n\n" + "\n".join(lines) + f"\n\nИтого: {order.total_amount}"
            send_mail(
                subject=f"Заказ #{order.id}",
                message=body,
                from_email=None,              # возьмётся DEFAULT_FROM_EMAIL
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception:
            pass

        return order
