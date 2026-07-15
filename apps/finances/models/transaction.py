from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Transaction(models.Model):
    """
    Representa un movimiento financiero realizado por una usuaria.

    Una transacción corresponde a un ingreso o un gasto asociado
    a una categoría específica.

    Responsibilities:
        - Registrar ingresos y gastos.
        - Asociar la transacción a una categoría.
        - Registrar el monto y la fecha de la transacción.
        - Almacenar una descripción opcional.
    """

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="Usuaria",
    )

    category = models.ForeignKey(
        "finance.Category",
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name="Categoría",
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01")),
        ],
        verbose_name="Monto",
        help_text="Valor de la transacción.",
    )

    transaction_date = models.DateField(
        verbose_name="Fecha de la transacción",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
        help_text="Descripción opcional de la transacción.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
    )

    class Meta:
        ordering = ["-transaction_date", "-created_at"]

        verbose_name = "Transacción"
        verbose_name_plural = "Transacciones"

        indexes = [
            models.Index(
                fields=["user", "-transaction_date"],
                name="transaction_user_date_idx",
            ),
            models.Index(
                fields=["user", "category"],
                name="transaction_user_category_idx",
            ),
        ]

    @property
    def is_income(self):
        """
        Indica si la transacción corresponde a un ingreso.

        Returns:
            bool: True si la categoría es de tipo ingreso.
        """
        return self.category.is_income

    @property
    def is_expense(self):
        """
        Indica si la transacción corresponde a un gasto.

        Returns:
            bool: True si la categoría es de tipo gasto.
        """
        return self.category.is_expense

    def __str__(self):
        return (
            f"{self.category.name} - "
            f"${self.amount} - "
            f"{self.transaction_date:%d/%m/%Y}"
        )
