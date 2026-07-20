from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F, Q

from apps.base.services.date_service import get_current_date
from apps.cycles.choices import CycleStatus


class Cycle(models.Model):
    """
    ## Representa un ciclo menstrual registrado por una usuaria.

    Un ciclo comienza cuando la usuaria registra el inicio de un período
    menstrual y finaliza cuando registra el siguiente.

    Además de almacenar las fechas del ciclo, este modelo proporciona
    información calculada como el día actual, el progreso y la fase
    correspondiente a una fecha determinada.

    Responsibilities:
        - Representar un ciclo menstrual.
        - Mantener la integridad de sus datos.
        - Proporcionar información calculada del ciclo.
    """

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="cycles",
        verbose_name="Usuaria",
    )

    start_date = models.DateField(
        verbose_name="Fecha de inicio",
        help_text="Fecha en la que comenzó el período menstrual.",
    )

    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de finalización",
        help_text="Se establece automáticamente cuando inicia el siguiente período.",
    )

    expected_length = models.PositiveSmallIntegerField(
        default=28,
        validators=[
            MinValueValidator(20),
            MaxValueValidator(45),
        ],
        verbose_name="Duración esperada",
        help_text=(
            "Se utiliza para estimar la duración del ciclo hasta conocer "
            "su duración real."
        ),
    )

    actual_length = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name="Duración real",
        help_text="Se calcula automáticamente al finalizar el ciclo.",
    )

    status = models.CharField(
    max_length=10,
    choices=CycleStatus.choices,
    default=CycleStatus.ACTIVE,
)


    notes = models.TextField(
        blank=True,
        verbose_name="Notas",
    )

    class Meta:
        ordering = ["-start_date"]
        verbose_name = "Ciclo"
        verbose_name_plural = "Ciclos"

        indexes = [
            models.Index(fields=["user", "-start_date"]),
        ]

        constraints = [
            models.CheckConstraint(
                condition=Q(end_date__isnull=True) | Q(end_date__gte=F("start_date")),
                name="cycle_end_date_after_start_date",
            ),
        ]


    # Properties


    @property
    def is_finished(self):
        return self.status == CycleStatus.COMPLETED

    @property
    def is_active(self):
        return self.status == CycleStatus.ACTIVE

    @property
    def day_number(self):
        """
        Obtiene el número de día del ciclo.

        Si el ciclo continúa activo, se calcula utilizando la fecha
        actual. Si el ciclo ya finalizó, se utiliza la fecha de
        finalización.

        Returns:
            int: Día correspondiente dentro del ciclo.
        """
        reference_date = get_current_date() if self.status == CycleStatus.ACTIVE else self.end_date
        return (reference_date - self.start_date).days + 1

    @property
    def progress_percentage(self):
        """
        Calcula el porcentaje de progreso del ciclo.

        Returns:
            int: Porcentaje de avance del ciclo.
        """
        return min(
            100,
            round((self.day_number / self.expected_length) * 100),
        )

    @property
    def current_phase(self):
        """
        Obtiene la fase correspondiente al día actual.

        Returns:
            Phase | None: Fase actual del ciclo.
        """
        return self.get_phase_for_date(get_current_date())


    # Public methods

    def get_phase_for_date(self, target_date):
        cycle_phase = self.phases.filter(
            start_date__lte=target_date,
            end_date__gte=target_date,
        ).first()

        if cycle_phase is not None:
            return cycle_phase.phase

        last = self.phases.order_by("-end_date").first()
        return last.phase if last else None

    def __str__(self):
        return f"Ciclo de {self.user.full_name} ({self.start_date:%d/%m/%Y})"
