"""
Servicio encargado de la lógica de negocio relacionada con los ciclos menstruales.

Responsibilities:
- Registrar el inicio de un nuevo período menstrual.
- Crear nuevos ciclos menstruales.
- Finalizar automáticamente el ciclo anterior.
- Calcular la duración real del ciclo.
- Consultar ciclos según diferentes criterios.
- Consultar las fases de un ciclo según una fecha determinada.

Notes:
- Este módulo únicamente contiene lógica de negocio.
- No debe contener lógica de vistas, formularios o peticiones HTTP.
- Solo puede existir un ciclo activo por usuaria.
"""

from datetime import date, timedelta
from typing import Any
from django.db import transaction
from django.db.models import QuerySet

from apps.cycles.choices import CycleStatus, EnergyLevel, Mood
from apps.cycles.models import Cycle, CyclePhase
from apps.cycles.models.daily_log import DailyLog
from apps.cycles.models.phase import Phase
from apps.cycles.models.symptom import Symptom
from apps.insights.services.insight_service import generate_insight
from apps.cycles.services.daily_log_service import create_daily_log, get_daily_log_by_date, update_daily_log
from apps.users.models import User


def calculate_cycle_length(
    start_date: date,
    next_start_date: date,
) -> int:
    """
    Calcula la duración real de un ciclo menstrual.

    Args:
        start_date (date):
            Fecha de inicio del ciclo.

        next_start_date (date):
            Fecha de inicio del siguiente ciclo.

    Returns:
        int:
            Número de días transcurridos entre ambas fechas.

    Raises:
        ValueError:
            Si la fecha del siguiente ciclo no es posterior a la fecha de inicio.

    Notes:
        La duración del ciclo corresponde al número de días entre el
        primer día de una menstruación y el primer día de la siguiente.
    """
    if next_start_date <= start_date:
        raise ValueError(
            "La fecha del siguiente ciclo debe ser posterior a la fecha de inicio."
        )

    delta = next_start_date - start_date

    return delta.days


def get_active_cycle(user: User) -> Cycle | None:
    """
    Obtiene el ciclo menstrual activo de una usuaria.

    Args:
        user (User):
            Usuaria propietaria del ciclo.

    Returns:
        Cycle | None:
            El ciclo activo si existe; de lo contrario, None.

    Notes:
        Solo puede existir un ciclo activo por usuaria.
    """
    return (
        Cycle.objects.filter(
            user=user,
            status=CycleStatus.ACTIVE,
        )
        .first()
    )


def get_previous_cycle(cycle: Cycle) -> Cycle | None:
    """
    Obtiene el ciclo menstrual inmediatamente anterior al ciclo recibido.

    Args:
        cycle (Cycle):
            Ciclo de referencia.

    Returns:
        Cycle | None:
            El ciclo anterior si existe; de lo contrario, None.

    Notes:
        La búsqueda se realiza utilizando la fecha de inicio del ciclo y el
        orden definido en el modelo.
    """
    return (
        Cycle.objects.filter(
            user=cycle.user,
            start_date__lt=cycle.start_date,
        )
        .first()
    )


def get_cycle_by_date(
    user: User,
    target_date: date,
) -> Cycle | None:
    """
    Obtiene el ciclo menstrual al que pertenece una fecha determinada.

    Args:
        user (User):
            Usuaria propietaria del ciclo.

        target_date (date):
            Fecha que se desea consultar.

    Returns:
        Cycle | None:
            Ciclo al que pertenece la fecha indicada o None si no existe.

    Notes:
        La búsqueda se realiza utilizando el rango comprendido entre la
        fecha de inicio y la fecha de finalización del ciclo.
    """
    return (
        Cycle.objects.filter(
            user=user,
            start_date__lte=target_date,
            end_date__gte=target_date,
        ).first()
    )


def get_cycle_phase_by_date(
    cycle: Cycle,
    target_date: date,
) -> CyclePhase | None:
    """
    Obtiene la fase del ciclo menstrual correspondiente a una fecha determinada.

    Args:
        cycle (Cycle):
            Ciclo menstrual donde se realizará la búsqueda.

        target_date (date):
            Fecha que se desea consultar.

    Returns:
        CyclePhase | None:
            Fase del ciclo correspondiente a la fecha indicada o None si
            no existe.

    Notes:
        La búsqueda se realiza utilizando el rango comprendido entre la
        fecha de inicio y la fecha de finalización de cada fase del ciclo.
    """
    return (
        CyclePhase.objects.filter(
            cycle=cycle,
            start_date__lte=target_date,
            end_date__gte=target_date,
        )
        .first()
    )


def get_dashboard_data(user: User) -> dict[str, Any]:
    """
    Obtiene la información necesaria para mostrar el dashboard
    principal de la usuaria.

    Args:
        user (User):
            Usuaria propietaria del dashboard.

    Returns:
        dict[str, Any]:
            Diccionario con la información del ciclo activo,
            fase actual, registro diario de hoy y el progreso
            de la fase actual.

    Notes:
        Si la usuaria no tiene un ciclo activo, los valores
        relacionados con el ciclo serán ``None``.
    """

    today = date.today()

    active_cycle = get_active_cycle(user)

    today_log = None
    current_phase = None
    phase_day = None
    days_remaining = None

    if active_cycle:
        current_phase = active_cycle.current_phase

        today_log = get_daily_log_by_date(
            active_cycle,
            today,
        )

        phase_record = active_cycle.phases.filter(
            start_date__lte=today,
            end_date__gte=today,
        ).first()

        if phase_record:
            phase_day = (
                today - phase_record.start_date
            ).days + 1

            days_remaining = (
                phase_record.end_date - today
            ).days

    return {
        "active_cycle": active_cycle,
        "current_phase": current_phase,
        "today_log": today_log,
        "phase_day": phase_day,
        "days_remaining": days_remaining,
    }


def create_or_update_daily_log(
    user: User,
    energy_level: EnergyLevel | None = None,
    mood: Mood | None = None,
    notes: str = "",
    symptoms: list[Symptom] | None = None,
) -> DailyLog:
    """
    Crea o actualiza el registro diario correspondiente
    a la fecha actual.

    Args:
        user (User):
            Usuaria propietaria del registro.

        energy_level (EnergyLevel | None):
            Nivel de energía registrado.

        mood (Mood | None):
            Estado de ánimo registrado.

        notes (str):
            Notas adicionales del día.

        symptoms (list[Symptom] | None):
            Lista de síntomas asociados al registro.

    Returns:
        DailyLog:
            Registro diario creado o actualizado.

    Raises:
        ValueError:
            Si la usuaria no posee un ciclo activo.

    Notes:
        Si ya existe un registro para la fecha actual,
        este será actualizado. En caso contrario,
        se creará un nuevo registro.
    """

    today = date.today()

    active_cycle = get_active_cycle(user)

    if active_cycle is None:
        raise ValueError(
            "La usuaria no tiene un ciclo activo."
        )

    daily_log = get_daily_log_by_date(
        active_cycle,
        today,
    )

    if daily_log:
        return update_daily_log(
            daily_log=daily_log,
            energy_level=energy_level,
            mood=mood,
            notes=notes,
            symptoms=symptoms,
        )

    return create_daily_log(
        cycle=active_cycle,
        log_date=today,
        energy_level=energy_level,
        mood=mood,
        notes=notes,
        symptoms=symptoms,
    )


def get_cycle_history(
    user: User,
) -> QuerySet[Cycle]:
    """
    Obtiene el historial de ciclos de una usuaria.

    Args:
        user (User):
            Usuaria propietaria de los ciclos.

    Returns:
        QuerySet[Cycle]:
            Historial de ciclos de la usuaria.
    """

    return Cycle.objects.filter(
        user=user,
    )


@transaction.atomic
def register_period(
    user: User,
    start_date: date,
) -> Cycle:
    """
    Registra el inicio de un nuevo período menstrual.

    Args:
        user (User):
            Usuaria que registra el período.

        start_date (date):
            Fecha de inicio del nuevo período.

    Returns:
        Cycle:
            Nuevo ciclo menstrual creado.

    Notes:
        Si existe un ciclo activo, este será finalizado antes de crear
        el nuevo ciclo. La duración real del ciclo finalizado se utilizará
        como duración esperada del siguiente ciclo.
    """

    active_cycle = (
        Cycle.objects.select_for_update()
        .filter(
            user=user,
            status=CycleStatus.ACTIVE,
        )
        .first()
    )

    if active_cycle:

        _close_previous_cycle(
            cycle=active_cycle,
            next_period_date=start_date,
        )

        actual_length = active_cycle.actual_length

        if actual_length is None:
            raise ValueError(
                "El ciclo debe tener una duración real antes de crear un nuevo ciclo."
            )

        user.predicted_cycle_length = actual_length

        user.save(
            update_fields=[
                "predicted_cycle_length",
            ]
        )

        expected_length = actual_length

    else:
        expected_length = user.predicted_cycle_length

    return _create_cycle(
        user=user,
        start_date=start_date,
        expected_length=expected_length,
    )


def _create_cycle(
    user: User,
    start_date: date,
    expected_length: int,
) -> Cycle:
    """
    Crea un nuevo ciclo menstrual.

    Args:
        user (User):
            Usuaria propietaria del ciclo.

        start_date (date):
            Fecha de inicio del ciclo.

        expected_length (int):
            Duración esperada del ciclo en días.

    Returns:
        Cycle:
            Ciclo menstrual creado.

    Notes:
        La fecha de finalización se calcula utilizando la duración
        esperada del ciclo. Cuando la usuaria registre un nuevo
        período, esta fecha será reemplazada por la fecha real de
        finalización.
    """

    estimated_end_date = (
        start_date +
        timedelta(days=expected_length - 1)
    )

    cycle = Cycle.objects.create(
        user=user,
        start_date=start_date,
        end_date=estimated_end_date,
        expected_length=expected_length,
        actual_length=None,
        status=CycleStatus.ACTIVE,
    )

    _generate_cycle_phases(cycle)

    return cycle


@transaction.atomic
def _generate_cycle_phases(cycle: Cycle) -> None:
    """Genera y crea los CyclePhase para un ciclo según las Phase maestras."""
    total_days = (cycle.end_date - cycle.start_date).days + 1
    phases = Phase.objects.all().order_by("sort_order")
    num_phases = len(phases)

    if num_phases == 0:
        return

    phase_start = cycle.start_date
    phase_list = list(phases)

    for i, phase in enumerate(phase_list):
        if i < num_phases - 1:
            phase_days = max(
                round(total_days * float(phase.estimated_percentage) / 100),
                1,
            )
        else:
            phase_days = max(
                total_days - (phase_start - cycle.start_date).days,
                1,
            )

        phase_end = phase_start + timedelta(days=phase_days - 1)

        CyclePhase.objects.create(
            cycle=cycle,
            phase=phase,
            start_date=phase_start,
            end_date=phase_end,
        )

        phase_start = phase_end + timedelta(days=1)


def _close_previous_cycle(
    cycle: Cycle,
    next_period_date: date,
) -> None:
    """
    Finaliza un ciclo menstrual activo.

    Args:
        cycle (Cycle):
            Ciclo que será finalizado.

        next_period_date (date):
            Fecha de inicio del siguiente ciclo.

    Returns:
        None

    Notes:
        Actualiza la duración real del ciclo, reemplaza la fecha estimada
        de finalización por la fecha real y marca el ciclo como completado.
    """

    cycle.actual_length = calculate_cycle_length(
        start_date=cycle.start_date,
        next_start_date=next_period_date,
    )

    cycle.end_date = (
        next_period_date -
        timedelta(days=1)
    )

    cycle.status = CycleStatus.COMPLETED

    cycle.save(
        update_fields=[
            "actual_length",
            "end_date",
            "status",
        ]
    )

    generate_insight(cycle)

