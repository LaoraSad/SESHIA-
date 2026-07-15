from django.db import models
from choices import InsightType


class Insight(models.Model):
    """
    Representa un insight mostrado a una usuaria.

    Un insight es una recomendación personalizada generada por el sistema
    a partir del análisis de ciclos anteriores, registros diarios y
    transacciones financieras.

    Los insights almacenados corresponden únicamente a aquellos que ya
    fueron mostrados a la usuaria, permitiendo mantener un historial de
    recomendaciones.

    Responsibilities:
        - Almacenar el historial de insights mostrados.
        - Relacionar el insight con el ciclo y la fase analizados.
        - Identificar el tipo de análisis realizado.
        - Registrar la fecha en que el insight fue mostrado.
    """

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="insights",
        verbose_name="Usuaria",
    )

    cycle = models.ForeignKey(
        "cycle.Cycle",
        on_delete=models.CASCADE,
        related_name="insights",
        verbose_name="Ciclo",
        help_text="Ciclo menstrual utilizado para generar el insight.",
    )

    phase = models.ForeignKey(
        "cycle.Phase",
        on_delete=models.PROTECT,
        related_name="insights",
        verbose_name="Fase",
        help_text="Fase del ciclo sobre la que trata el insight.",
    )

    type = models.CharField(
        max_length=20,
        choices=InsightType.choices,
        verbose_name="Tipo",
        help_text="Clasificación del insight.",
    )

    title = models.CharField(
        max_length=100,
        verbose_name="Título",
        help_text="Título corto que resume el insight.",
    )

    message = models.TextField(
        verbose_name="Mensaje",
        help_text="Contenido del insight mostrado a la usuaria.",
    )

    shown_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de visualización",
    )

    class Meta:
        ordering = ["-shown_at"]

        verbose_name = "Insight"
        verbose_name_plural = "Insights"

        indexes = [
            models.Index(
                fields=["user", "-shown_at"],
                name="insight_user_date_idx",
            ),
            models.Index(
                fields=["user", "type"],
                name="insight_user_type_idx",
            ),
        ]

    def __str__(self):
        return (
            f"{self.title} - "
            f"{self.shown_at:%d/%m/%Y}"
        )
