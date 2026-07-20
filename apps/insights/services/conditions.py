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
from decimal import Decimal

from django.db.models import Avg, Count, Sum

from apps.cycles.choices import EnergyLevel, Mood
from apps.cycles.models import Cycle, DailyLog
from apps.finances.choices import CategoryType
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

    return cycle.transactions.filter(
        is_active=True,
    )

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
def previous_cycle_low_energy(cycle):
    previous_cycle = get_previous_cycle(cycle)

    if previous_cycle is None:
        return False

    low_energy_logs = previous_cycle.daily_logs.filter(
        energy_level__lte=EnergyLevel.LOW,
    )

    if not low_energy_logs.exists():
        return False

    phases = set()
    for log in low_energy_logs:
        if log.phase:
            phases.add(log.phase.name)

    if phases:
        return ", ".join(sorted(phases))

    return True


def previous_cycle_high_energy(cycle) -> bool:
    """
    Determina si en el ciclo anterior la usuaria registró
    niveles altos de energía durante la fase ovulatoria.

    Args:
        cycle:
            Ciclo actual.

    Returns:
        bool:
            True si existe al menos un registro con
            energía alta en la fase ovulatoria.
    """

    previous_cycle = get_previous_cycle(cycle)

    if previous_cycle is None:
        return False

    for daily_log in get_cycle_daily_logs(previous_cycle):

        if (
            daily_log.phase
            and daily_log.phase.name.lower() == "ovulatoria"
            and daily_log.energy_level == EnergyLevel.HIGH
        ):
            return True

    return False


def previous_cycle_mood_pattern(cycle) -> bool:
    """
    Determina si durante la fase lútea del ciclo anterior
    se registró al menos un estado de ánimo.

    Args:
        cycle:
            Ciclo actual.

    Returns:
        bool:
            True si existe un registro de estado de ánimo.
    """

    previous_cycle = get_previous_cycle(cycle)

    if previous_cycle is None:
        return False

    for daily_log in get_cycle_daily_logs(previous_cycle):

        if (
            daily_log.phase
            and daily_log.phase.name.lower() == "lútea"
            and daily_log.mood
        ):
            return True

    return False


def previous_cycle_symptoms(cycle) -> bool:
    """
    Determina si el ciclo anterior contiene
    registros con síntomas.

    Args:
        cycle:
            Ciclo actual.

    Returns:
        bool:
            True si existe al menos un síntoma registrado.
    """

    previous_cycle = get_previous_cycle(cycle)

    if previous_cycle is None:
        return False

    return previous_cycle.daily_logs.filter(
        symptoms__isnull=False,
    ).exists()


def multiple_previous_cycle_symptoms(cycle) -> bool:
    """
    Determina si el ciclo anterior contiene
    varios registros con síntomas.

    Args:
        cycle:
            Ciclo actual.

    Returns:
        bool:
            True si existen dos o más registros
            con síntomas.
    """

    previous_cycle = get_previous_cycle(cycle)

    if previous_cycle is None:
        return False

    return (
        previous_cycle.daily_logs.filter(
            symptoms__isnull=False,
        )
        .distinct()
        .count()
        >= 2
    )


def consistent_daily_logs(cycle) -> bool:
    """
    Determina si la usuaria registró información
    de forma constante durante el ciclo.

    Args:
        cycle:
            Ciclo a evaluar.

    Returns:
        bool:
            True si existen registros en al menos
            la mitad de los días esperados.
    """

    total_logs = cycle.daily_logs.count()

    return total_logs >= (cycle.expected_length / 2)


def insufficient_daily_logs(cycle) -> bool:
    """
    Determina si existen pocos registros diarios.

    Args:
        cycle:
            Ciclo a evaluar.

    Returns:
        bool:
            True si los registros son insuficientes.
    """

    return not consistent_daily_logs(cycle)


def uses_notes_frequently(cycle) -> bool:
    """
    Determina si la usuaria utiliza con frecuencia
    las notas de los registros diarios.

    Args:
        cycle:
            Ciclo a evaluar.

    Returns:
        bool:
            True si existen al menos tres registros
            con notas.
    """

    return (
        cycle.daily_logs.exclude(
            notes="",
        ).count()
        >= 3
    )


def _total_expenses(cycle) -> Decimal:
    """
    Calcula el total de gastos registrados en un ciclo.

    Args:
        cycle:
            Ciclo a evaluar.

    Returns:
        Decimal:
            Total de gastos del ciclo.
    """

    total = Decimal("0.00")

    for transaction in get_cycle_transactions(cycle):

        if transaction.is_expense:
            total += transaction.amount

    return total


# Current Cycle Conditions
def current_consecutive_low_energy(cycle):
    logs = cycle.daily_logs.filter(
        energy_level__isnull=False,
    ).order_by("-log_date")

    if not logs.exists():
        return False

    count = 0
    for log in logs:
        if log.energy_level <= EnergyLevel.LOW:
            count += 1
        else:
            break

    if count >= 3:
        return str(count)

    return False


def current_most_frequent_mood(cycle):
    logs = cycle.daily_logs.exclude(
        mood__isnull=True,
    ).exclude(mood="")

    if not logs.exists():
        return False

    total = logs.count()
    mood_counts = {}
    for log in logs:
        mood_counts[log.mood] = mood_counts.get(log.mood, 0) + 1

    most_common = max(mood_counts, key=mood_counts.get)
    percentage = mood_counts[most_common] / total

    if percentage >= 0.5:
        return dict(Mood.choices).get(most_common, most_common)

    return False


def current_logging_streak(cycle):
    logs = cycle.daily_logs.order_by("-log_date")
    if not logs.exists():
        return False

    count = 1
    for i in range(len(logs) - 1):
        if (logs[i].log_date - logs[i + 1].log_date).days == 1:
            count += 1
        else:
            break

    if count >= 5:
        return str(count)

    return False


def current_repeated_symptom(cycle):
    from django.db.models import Count

    symptom_counts = (
        cycle.daily_logs.exclude(symptoms=None)
        .values("symptoms__name")
        .annotate(count=Count("symptoms"))
        .filter(count__gte=2)
    )

    if symptom_counts.exists():
        return symptom_counts.first()["symptoms__name"]

    return False


# Finance Conditions
def higher_total_expenses(cycle) -> bool:
    """
    Determina si los gastos del ciclo actual son
    mayores que los del ciclo anterior.

    Args:
        cycle:
            Ciclo actual.

    Returns:
        bool:
            True si los gastos aumentaron.
    """

    previous_cycle = get_previous_cycle(cycle)

    if previous_cycle is None:
        return False

    return (
        _total_expenses(cycle)
        >
        _total_expenses(previous_cycle)
    )


def lower_total_expenses(cycle) -> bool:
    """
    Determina si los gastos del ciclo actual son
    menores que los del ciclo anterior.

    Args:
        cycle:
            Ciclo actual.

    Returns:
        bool:
            True si los gastos disminuyeron.
    """

    previous_cycle = get_previous_cycle(cycle)

    if previous_cycle is None:
        return False

    return (
        _total_expenses(cycle)
        <
        _total_expenses(previous_cycle)
    )


def stable_expense_pattern(cycle) -> bool:
    """
    Determina si el gasto total del ciclo se
    mantiene similar al del ciclo anterior.

    Args:
        cycle:
            Ciclo actual.

    Returns:
        bool:
            True si la diferencia es menor o igual al 10 %.
    """

    previous_cycle = get_previous_cycle(cycle)

    if previous_cycle is None:
        return False

    previous_total = _total_expenses(previous_cycle)

    if previous_total == 0:
        return False

    current_total = _total_expenses(cycle)

    difference = abs(current_total - previous_total)

    return (
        (difference / previous_total)
        <= Decimal("0.10")
    )


def insufficient_transactions(cycle) -> bool:
    """
    Determina si existen pocas transacciones
    registradas en el ciclo.

    Args:
        cycle:
            Ciclo actual.

    Returns:
        bool:
            True si existen menos de cinco
            transacciones.
    """

    return (
        cycle.transactions.filter(is_active=True).count() < 5
    )


# Mixed Conditions
def previous_cycle_low_energy_with_higher_expenses(cycle) -> bool:
    """
    Determina si la usuaria presenta un patrón de
    baja energía junto con un aumento en los gastos.

    Args:
        cycle:
            Ciclo actual.

    Returns:
        bool:
            True si ambas condiciones se cumplen.
    """

    return (
        previous_cycle_low_energy(cycle)
        and higher_total_expenses(cycle)
    )


def mood_related_expenses(cycle) -> bool:
    """
    Determina si existen registros de estado de
    ánimo junto con un incremento en los gastos.

    Args:
        cycle:
            Ciclo actual.

    Returns:
        bool:
            True si ambas condiciones se cumplen.
    """

    return (
        previous_cycle_mood_pattern(cycle)
        and higher_total_expenses(cycle)
    )


def high_energy_with_stable_expenses(cycle) -> bool:
    """
    Determina si existe un patrón de energía alta
    acompañado de estabilidad financiera.

    Args:
        cycle:
            Ciclo actual.

    Returns:
        bool:
            True si ambas condiciones se cumplen.
    """

    return (
        previous_cycle_high_energy(cycle)
        and stable_expense_pattern(cycle)
    )


def enough_data_for_mixed_analysis(cycle) -> bool:
    """
    Determina si existe suficiente información
    para generar insights combinados.

    Args:
        cycle:
            Ciclo actual.

    Returns:
        bool:
            True si existen registros diarios y
            transacciones suficientes.
    """

    return (
        consistent_daily_logs(cycle)
        and not insufficient_transactions(cycle)
    )


def _has_category_expenses_in_phase(cycle, category_names, phase_name):
    """Helper: True si el ciclo tiene gastos en categorias dadas durante una fase."""
    return cycle.transactions.filter(
        is_active=True,
        category__name__in=category_names,
        category__category_type=CategoryType.EXPENSE,
        cycle_phase__phase__name__iexact=phase_name,
    ).exists()


def repeated_wellness_expenses(cycle) -> bool:
    """
    Determina si la usuaria suele gastar en bienestar
    durante la fase menstrual en ciclos consecutivos.
    """
    previous_cycle = get_previous_cycle(cycle)

    if previous_cycle is None:
        return False

    wellness_names = ["Cuidado menstrual", "Compras", "Ocio"]

    return (
        _has_category_expenses_in_phase(cycle, wellness_names, "menstrual")
        and _has_category_expenses_in_phase(previous_cycle, wellness_names, "menstrual")
    )


def repeated_food_expenses(cycle) -> bool:
    """
    Determina si la usuaria suele gastar más en alimentación
    durante la fase lútea en ciclos consecutivos.
    """
    previous_cycle = get_previous_cycle(cycle)

    if previous_cycle is None:
        return False

    return (
        _has_category_expenses_in_phase(cycle, ["Alimentación"], "lútea")
        and _has_category_expenses_in_phase(previous_cycle, ["Alimentación"], "lútea")
    )


def symptoms_related_expenses(cycle) -> bool:
    """
    Determina si los síntomas durante la fase menstrual
    coinciden con gastos en bienestar.
    """
    previous_cycle = get_previous_cycle(cycle)

    if previous_cycle is None:
        return False

    has_symptoms = previous_cycle.daily_logs.filter(
        log_date__gte=previous_cycle.start_date,
        symptoms__isnull=False,
    ).exists()

    if not has_symptoms:
        return False

    return _has_category_expenses_in_phase(
        previous_cycle,
        ["Cuidado menstrual", "Compras", "Ocio"],
        "menstrual",
    )


def repeated_phase_pattern(cycle) -> bool:
    """
    Determina si existe un patrón repetitivo combinando
    registros diarios y financieros en la fase lútea.
    """
    previous_cycle = get_previous_cycle(cycle)

    if previous_cycle is None:
        return False

    luteal_phase = previous_cycle.phases.filter(
        phase__name__iexact="lútea",
    ).first()

    if luteal_phase is None:
        return False

    has_daily_logs = previous_cycle.daily_logs.filter(
        log_date__gte=luteal_phase.start_date,
        log_date__lte=luteal_phase.end_date,
    ).exists()

    has_transactions = previous_cycle.transactions.filter(
        is_active=True,
        transaction_date__gte=luteal_phase.start_date,
        transaction_date__lte=luteal_phase.end_date,
    ).exists()

    return has_daily_logs and has_transactions


CONDITIONS = {
    # Cycle
    "has_enough_cycle_history": has_enough_cycle_history,
    "stable_cycle_duration": stable_cycle_duration,
    "variable_cycle_duration": variable_cycle_duration,
    "insufficient_cycle_history": insufficient_cycle_history,
    "has_extended_cycle_history": has_extended_cycle_history,
    "stable_cycle_trend": stable_cycle_trend,
    "changing_cycle_trend": changing_cycle_trend,
    "not_enough_cycles_for_analysis": not_enough_cycles_for_analysis,

    # Daily Log
    "previous_cycle_low_energy": previous_cycle_low_energy,
    "previous_cycle_high_energy": previous_cycle_high_energy,
    "previous_cycle_mood_pattern": previous_cycle_mood_pattern,
    "previous_cycle_symptoms": previous_cycle_symptoms,
    "multiple_previous_cycle_symptoms": multiple_previous_cycle_symptoms,
    "consistent_daily_logs": consistent_daily_logs,
    "insufficient_daily_logs": insufficient_daily_logs,
    "uses_notes_frequently": uses_notes_frequently,
    "current_consecutive_low_energy": current_consecutive_low_energy,
    "current_most_frequent_mood": current_most_frequent_mood,
    "current_logging_streak": current_logging_streak,
    "current_repeated_symptom": current_repeated_symptom,

    # Finance
    "higher_total_expenses": higher_total_expenses,
    "lower_total_expenses": lower_total_expenses,
    "stable_expense_pattern": stable_expense_pattern,
    "insufficient_transactions": insufficient_transactions,
    "repeated_wellness_expenses": repeated_wellness_expenses,
    "repeated_food_expenses": repeated_food_expenses,

    # Mixed
    "previous_cycle_low_energy_with_higher_expenses": previous_cycle_low_energy_with_higher_expenses,
    "mood_related_expenses": mood_related_expenses,
    "high_energy_with_stable_expenses": high_energy_with_stable_expenses,
    "enough_data_for_mixed_analysis": enough_data_for_mixed_analysis,
    "symptoms_related_expenses": symptoms_related_expenses,
    "repeated_phase_pattern": repeated_phase_pattern,
}

