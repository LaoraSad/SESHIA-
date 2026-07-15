from django.db import models
from django.db.models import Q
from choices import CategoryType


class Category(models.Model):
    """
    Representa una categoría utilizada para clasificar las transacciones.

    Existen dos tipos de categorías:

        - Categorías del sistema (is_default=True, user=None)
        - Categorías personalizadas creadas por la usuaria.

    Responsibilities:
        - Clasificar ingresos y gastos.
        - Permitir categorías predeterminadas y personalizadas.
        - Facilitar la organización de las transacciones.
    """

    name = models.CharField(
        max_length=80,
        verbose_name="Nombre",
    )

    category_type = models.CharField(
        max_length=10,
        choices=CategoryType.choices,
        verbose_name="Tipo",
    )

    icon = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Ícono",
        help_text="Emoji representativo de la categoría.",
    )

    is_default = models.BooleanField(
        default=True,
        verbose_name="Categoría del sistema",
        help_text="Indica si la categoría fue creada por el sistema.",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Activa",
        help_text="Permite ocultar la categoría sin eliminarla.",
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="categories",
        null=True,
        blank=True,
        verbose_name="Usuaria",
        help_text="Se deja vacío para las categorías predeterminadas.",
    )

    class Meta:
        ordering = ["name"]

        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

        indexes = [
            models.Index(
                fields=["user", "category_type"],
                name="category_user_type_idx",
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "category_type", "name"],
                name="unique_category_per_user",
            ),
            models.CheckConstraint(
                condition=(
                    Q(is_default=True, user__isnull=True) |
                    Q(is_default=False, user__isnull=False)
                ),
                name="category_default_user_consistency",
            ),
        ]

    @property
    def is_income(self):
        """
        Indica si la categoría corresponde a un ingreso.
        """
        return self.category_type == CategoryType.INCOME

    @property
    def is_expense(self):
        """
        Indica si la categoría corresponde a un gasto.
        """
        return self.category_type == CategoryType.EXPENSE

    def __str__(self):
        return self.name
