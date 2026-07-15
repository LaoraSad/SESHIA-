from django.db import models


class SymptomCategory(models.Model):
    """
    Representa una categoría de síntomas.

    Este modelo funciona como una tabla maestra para organizar
    los síntomas que la usuaria puede registrar diariamente.

    Responsibilities:
        - Organizar los síntomas por categorías.
        - Definir el orden de visualización.
        - Almacenar información descriptiva de la categoría.
    """

    name = models.CharField(
        max_length=80,
        unique=True,
        verbose_name="Nombre",
    )

    icon = models.CharField(
        max_length=10,
        blank=True,
        verbose_name="Ícono",
        help_text="Emoji representativo de la categoría.",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
    )

    sort_order = models.PositiveSmallIntegerField(
        unique=True,
        verbose_name="Orden",
    )

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Categoría de síntoma"
        verbose_name_plural = "Categorías de síntomas"

    def __str__(self):
        return self.name

