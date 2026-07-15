from django.db import models
from django.db.models import F, Q


class CyclePhase(models.Model):
    """
    Representa una fase específica dentro de un ciclo menstrual.

    Cada registro relaciona un ciclo con una de sus fases,
    indicando las fechas en las que dicha fase ocurre.

    Responsibilities:
        - Relacionar un ciclo con una fase.
        - Almacenar las fechas de inicio y fin de la fase.
        - Facilitar la consulta de la fase correspondiente a una fecha.
    """

    cycle = models.ForeignKey(
        "cycles.Cycle",
        on_delete=models.CASCADE,
        related_name="phases",
        verbose_name="Ciclo",
    )

    phase = models.ForeignKey(
        "cycles.Phase",
        on_delete=models.CASCADE,
        verbose_name="Fase",
    )

    start_date = models.DateField(
        verbose_name="Fecha de inicio",
    )

    end_date = models.DateField(
        verbose_name="Fecha de finalización",
    )

    class Meta:
        ordering = ["start_date"]

        verbose_name = "Fase del ciclo"
        verbose_name_plural = "Fases del ciclo"

        indexes = [
            models.Index(
                fields=["cycle", "start_date", "end_date"],
                name="cycle_phase_date_idx",
            ),
        ]

        constraints = [
            models.CheckConstraint(
            condition=Q(end_date__gte=F("start_date")),
            name="cycle_phase_end_after_start",
            ),
            models.UniqueConstraint(
                fields=["cycle", "phase"],
                name="unique_phase_per_cycle",
            ),
        ]

    def __str__(self):
        return (
            f"{self.phase.name}: "
            f"{self.start_date:%d/%m/%Y} - "
            f"{self.end_date:%d/%m/%Y}"
        )
