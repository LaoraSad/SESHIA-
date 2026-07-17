"""
Funciones encargadas de evaluar las condiciones utilizadas
para generar insights.

Cada función representa una condición específica asociada
a una regla definida en `rules.py`.

Responsibilities:
    - Evaluar información del ciclo menstrual.
    - Evaluar registros diarios.
    - Evaluar información financiera.
    - Evaluar condiciones combinadas.

Notes:
    - No genera insights.
    - No crea registros en la base de datos.
    - No contiene lógica de presentación.
"""

from datetime import timedelta

from django.db.models import Avg, Count, Sum

from apps.cycles.choices import EnergyLevel
from apps.cycles.models import Cycle, DailyLog
from apps.finances.models import Transaction


# Helper functions
def get_previous_cycle(cycle):
    """
    Obtiene el ciclo inmediatamente anterior de la usuaria.

    Args:
        cycle:
            Ciclo actual.

    Returns:
        Cycle | None:
            Ciclo anterior o None si no existe.
    """

    return (
        Cycle.objects.filter(
            user=cycle.user,
            start_date__lt=cycle.start_date,
        ).first()
    )


def get_cycle_daily_logs(cycle):
    """
    Obtiene los registros diarios de un ciclo.

    Args:
        cycle:
            Ciclo a consultar.

    Returns:
        QuerySet[DailyLog]:
            Registros diarios del ciclo.
    """

    return cycle.daily_logs.all()


def get_cycle_transactions(cycle):
    """
    Obtiene las transacciones asociadas a un ciclo.

    Args:
        cycle:
            Ciclo a consultar.

    Returns:
        QuerySet[Transaction]:
            Transacciones registradas en el ciclo.
    """

    return cycle.transactions.all()

#Cycle Conditions
def has_enough_cycle_history(user) -> bool:
    """
    Determina si la usuaria posee suficientes ciclos para
    comenzar a generar análisis personalizados.

    Args:
        user:
            Usuaria a evaluar.

    Returns:
        bool:
            True si existen al menos tres ciclos registrados.
    """

    return (
        Cycle.objects.filter(user=user).count() >= 3
    )


def insufficient_cycle_history(user) -> bool:
    """
    Determina si aún no existe suficiente historial para
    generar recomendaciones confiables.

    Args:
        user:
            Usuaria a evaluar.

    Returns:
        bool:
            True cuando existen menos de tres ciclos.
    """

    return (
        Cycle.objects.filter(user=user).count() < 3
    )


def stable_cycle_duration(user) -> bool:
    """
    Determina si la duración de los últimos ciclos
    registrados por la usuaria ha sido estable.

    Se considera estable cuando la diferencia entre
    el ciclo más corto y el más largo no supera
    tres días.

    Args:
        user:
            Usuaria a evaluar.

    Returns:
        bool:
            True si la duración de los ciclos es estable.
    """

    cycles = list(
        Cycle.objects.filter(
            user=user,
            actual_length__isnull=False,
        )[:3],
    )

    if len(cycles) < 3:
        return False

    durations = [
        cycle.actual_length
        for cycle in cycles
    ]

    return (
        max(durations) - min(durations)
    ) <= 3


def variable_cycle_duration(user) -> bool:
    """
    Determina si la duración de los últimos ciclos
    presenta variaciones importantes.

    Args:
        user:
            Usuaria a evaluar.

    Returns:
        bool:
            True si la duración del ciclo no ha sido estable.
    """

    return not stable_cycle_duration(user)


def has_extended_cycle_history(user) -> bool:
    """
    Determina si la usuaria posee un historial amplio
    de ciclos registrados.

    Args:
        user:
            Usuaria a evaluar.

    Returns:
        bool:
            True si existen al menos seis ciclos registrados.
    """

    return (
        Cycle.objects.filter(user=user).count() >= 6
    )


def stable_cycle_trend(user) -> bool:
    """
    Determina si el historial del ciclo muestra
    una tendencia estable.

    Args:
        user:
            Usuaria a evaluar.

    Returns:
        bool:
            True si existe suficiente historial y
            la duración del ciclo ha permanecido estable.
    """

    return (
        has_extended_cycle_history(user)
        and stable_cycle_duration(user)
    )


def changing_cycle_trend(user) -> bool:
    """
    Determina si el historial muestra cambios
    en la tendencia del ciclo.

    Args:
        user:
            Usuaria a evaluar.

    Returns:
        bool:
            True cuando existe historial suficiente
            pero la duración del ciclo no es estable.
    """

    return (
        has_extended_cycle_history(user)
        and not stable_cycle_duration(user)
    )


def not_enough_cycles_for_analysis(user) -> bool:
    """
    Determina si todavía no existe suficiente
    información para realizar análisis de tendencias.

    Args:
        user:
            Usuaria a evaluar.

    Returns:
        bool:
            True si existen menos de seis ciclos registrados.
    """

    return (
        not has_extended_cycle_history(user)
    )


#Daily Log Conditions
def repeated_low_energy(cycle) -> bool:
    """
    Determina si en el ciclo anterior la usuaria registró
    niveles bajos de energía durante la fase menstrual.

    Args:
        cycle:
            Ciclo actual.

    Returns:
        bool:
            True si existe al menos un registro con
            energía baja en la fase menstrual.
    """

    previous_cycle = get_previous_cycle(cycle)

    if previous_cycle is None:
        return False

    for daily_log in get_cycle_daily_logs(previous_cycle):

        if (
            daily_log.phase
            and daily_log.phase.name.lower() == "menstrual"
            and daily_log.energy_level == EnergyLevel.LOW
        ):
            return True

    return False