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

from apps.cycles.models import Cycle, DailyLog
from apps.finances.models import Transaction


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