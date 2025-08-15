from django.urls import path
from .views import FurnitureListView, FurnitureDetailView, OrdersView

urlpatterns = [
    path("furniture/", FurnitureListView.as_view(), name="furniture-list"),
    path("furniture/<int:id>/", FurnitureDetailView.as_view(), name="furniture-detail"),
    path("orders/", OrdersView.as_view(), name="orders"),
]
