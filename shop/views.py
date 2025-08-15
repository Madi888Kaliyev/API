# shop/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Furniture, Order
from .serializers import (
    FurnitureSerializer,
    OrderSerializer,          # для чтения заказов (GET)
    CreateOrderSerializer,    # для создания заказа (POST)
)


class FurnitureListView(generics.ListAPIView):
    """
    GET /api/furniture/
    (опционально) фильтрация по категории: /api/furniture/?category=table|chair|sofa
    """
    serializer_class = FurnitureSerializer

    def get_queryset(self):
        qs = Furniture.objects.all().order_by("id")
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category=category)
        return qs


class FurnitureDetailView(generics.RetrieveAPIView):
    """
    GET /api/furniture/<id>/
    """
    serializer_class = FurnitureSerializer
    queryset = Furniture.objects.all()
    lookup_field = "id"


class OrdersView(generics.ListCreateAPIView):
    """
      ПУТЬ ДЛЯ ЗАКАЗОВ

      Пример тела POST:
      {
        "email": "name_email@example.com",
        "items": [
          {"furniture": 1, "quantity": 2},
          {"furniture": 3, "quantity": 1}
        ]
      }
    
    """
    # для GET отдаём заказ (с суммой и позициями)
    def get_serializer_class(self):
        return OrderSerializer if self.request.method == "GET" else CreateOrderSerializer

    # queryset для DRF 
    def get_queryset(self):
        email = self.request.query_params.get("email")
        qs = (
            Order.objects
            .all()
            .prefetch_related("items__furniture")
            .order_by("-created_at")
        )
        # Если email не передали
        # поэтому возвращаем пусто.
        return qs.filter(email=email) if email else Order.objects.none()

    # Если GET без email 
    def list(self, request, *args, **kwargs):
        email = request.query_params.get("email")
        if not email:
            return Response(
                {"detail": "Передайте email как query-параметр: /api/orders/?email=you@example.com"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().list(request, *args, **kwargs)

    # Создание заказа 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()  # ожидаем что сериалайзер вернёт созданный заказ
        # Отдаём полноценное представление заказа 
        out = OrderSerializer(order)
        return Response(out.data, status=status.HTTP_201_CREATED)
