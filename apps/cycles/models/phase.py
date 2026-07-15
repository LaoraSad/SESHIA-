from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Phase(models.Model):
    """
    Representa una fase del ciclo menstrual.

    Este modelo funciona como una tabla maestra y almacena la
    configuración utilizada para generar automáticamente las fases
    de cada ciclo menstrual.

    Responsibilities:
        - Definir el nombre de cada fase.
        - Indicar el orden en el que ocurre.
        - Almacenar el porcentaje estimado de duración.
        - Proporcionar información descriptiva sobre la fase.
    """

    name = models.CharField(
        max_length=80,
        unique=True,
        verbose_name="Nombre"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
        help_text="Información educativa que puede mostrarse a la usuaria."
    )

    estimated_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
        verbose_name="Porcentaje estimado",
        help_text=(
            "Porcentaje aproximado que representa esta fase "
            "dentro del ciclo menstrual."
        ),
    )

    sort_order = models.PositiveSmallIntegerField(
        unique=True,
        verbose_name="Orden",
        help_text="Orden en el que aparece la fase durante el ciclo."
    )

    class Meta:
        ordering = ["sort_order"]
        verbose_name = "Fase"
        verbose_name_plural = "Fases"

    def __str__(self):
        return self.name

