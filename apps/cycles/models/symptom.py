from django.db import models

from apps.cycles.models.symptom_category import SymptomCategory


class Symptom(models.Model):
    """
    Representa un síntoma que la usuaria puede seleccionar
    durante el registro diario.

    Este modelo funciona como una tabla maestra.

    Responsibilities:
        - Definir los síntomas disponibles.
        - Agruparlos por categoría.
        - Mantener un orden de visualización.
    """

    category = models.ForeignKey(
        SymptomCategory,
        on_delete=models.PROTECT,
        related_name="symptoms",
        verbose_name="Categoría",
    )

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
    )

    sort_order = models.PositiveSmallIntegerField(
        verbose_name="Orden",
    )

    class Meta:
        ordering = [
            "category__sort_order",
            "sort_order",
            "name",
        ]

        verbose_name = "Síntoma"
        verbose_name_plural = "Síntomas"

        constraints = [
            models.UniqueConstraint(
                fields=["category", "sort_order"],
                name="unique_symptom_order_per_category",
            ),
        ]

    def __str__(self):
        return self.name

