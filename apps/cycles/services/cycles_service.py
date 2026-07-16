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

from datetime import date
from datetime import timedelta

from apps.cycles.choices import CycleStatus
from apps.cycles.models import Cycle
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

    return Cycle.objects.create(
        user=user,
        start_date=start_date,
        end_date=estimated_end_date,
        expected_length=expected_length,
        actual_length=None,
        status=CycleStatus.ACTIVE,
    )

