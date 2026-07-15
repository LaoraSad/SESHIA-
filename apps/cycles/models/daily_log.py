from django.db import models
from apps.cycles.choices import EnergyLevel, Mood

class DailyLog(models.Model):
    """
    Representa el registro diario de una usuaria durante un ciclo menstrual.

    Cada registro almacena la información correspondiente a un único día
    del ciclo.

    Responsibilities:
        - Registrar el estado diario de la usuaria.
        - Almacenar el nivel de energía.
        - Almacenar el estado de ánimo.
        - Registrar los síntomas presentes.
        - Servir como fuente de información para estadísticas e insights.
    """

    cycle = models.ForeignKey(
        "cycles.Cycle",
        on_delete=models.CASCADE,
        related_name="daily_logs",
        verbose_name="Ciclo",
    )

    log_date = models.DateField(
        verbose_name="Fecha del registro",
    )

    energy_level = models.PositiveSmallIntegerField(
        choices=EnergyLevel.choices,
        null=True,
        blank=True,
        verbose_name="Nivel de energía",
    )

    mood = models.CharField(
        max_length=20,
        choices=Mood.choices,
        null=True,
        blank=True,
        verbose_name="Estado de ánimo",
    )

    symptoms = models.ManyToManyField(
        "cycles.Symptom",
        blank=True,
        related_name="daily_logs",
        verbose_name="Síntomas",
    )

    notes = models.TextField(
        blank=True,
        verbose_name="Notas",
    )

    class Meta:
        ordering = ["log_date"]

        verbose_name = "Registro diario"
        verbose_name_plural = "Registros diarios"

        indexes = [
            models.Index(
                fields=["cycle", "log_date"],
                name="daily_log_date_idx",
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=["cycle", "log_date"],
                name="unique_daily_log_per_day",
            ),
        ]

    @property
    def day_number(self):
        """
        Obtiene el número de día del ciclo al que pertenece el registro.

        Returns:
            int: Día correspondiente dentro del ciclo.
        """
        return (self.log_date - self.cycle.start_date).days + 1

    @property
    def phase(self):
        """
        Obtiene la fase correspondiente a la fecha del registro.

        Returns:
            Phase | None: Fase del ciclo para ese día.
        """
        return self.cycle.get_phase_for_date(self.log_date)

    def __str__(self):
        return (
            f"{self.cycle.user.full_name} - "
            f"{self.log_date:%d/%m/%Y}"
        )

