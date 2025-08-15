from django.db import models


class Furniture(models.Model):
    CATEGORY_CHOICES = [
        ("table", "Table"),
        ("chair", "Chair"),
        ("sofa", "Sofa"),
        ("bed", "Bed"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=200, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # индексируем поле, по которому фильтруем
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, db_index=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.category})"

    class Meta:
        # дополнительный составной индекс не обязателен, но может пригодиться
        indexes = [
            models.Index(fields=["category"]),
        ]


class Order(models.Model):
    # индексы для выборок по email и сортировки по дате
    email = models.EmailField(db_index=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self) -> str:
        return f"Order #{self.id} — {self.email} — {self.total_amount}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    furniture = models.ForeignKey(Furniture, on_delete=models.PROTECT)
    # фиксируем цену на момент заказа
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def line_total(self):
        return self.price * self.quantity

    def __str__(self) -> str:
        return f"Item #{self.id} for Order #{self.order_id}"
