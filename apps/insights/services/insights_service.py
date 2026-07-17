"""
Servicios encargados de generar y consultar insights.

Responsibilities:
    - Generar insights personalizados.
    - Evaluar las reglas disponibles.
    - Seleccionar el insight más relevante.
    - Almacenar el historial de insights.
"""

from apps.insights.conditions import CONDITIONS
from apps.insights.models import Insight
from apps.insights.rules import ALL_RULES


def generate_insight(cycle):
    """
    Genera un insight para un ciclo menstrual.

    El servicio evalúa todas las reglas disponibles,
    selecciona la de mayor prioridad y almacena el
    insight generado.

    Args:
        cycle:
            Ciclo a analizar.

    Returns:
        Insight | None:
            Insight creado o None si ninguna regla aplica.
    """

    applicable_rules = _get_applicable_rules(cycle)

    if not applicable_rules:
        return None

    rule = _select_best_rule(applicable_rules)

    return _create_insight(cycle, rule)


def _get_applicable_rules(cycle):
    """
    Obtiene las reglas cuyas condiciones se cumplen.

    Args:
        cycle:
            Ciclo a analizar.

    Returns:
        list:
            Reglas aplicables.
    """

    applicable_rules = []

    for rule in ALL_RULES:
        condition_func = CONDITIONS.get(rule.condition)

        if condition_func is None:
            continue

        if condition_func(cycle):
            applicable_rules.append(rule)

    return applicable_rules


def _select_best_rule(rules):
    """
    Selecciona la regla con mayor prioridad.

    Args:
        rules:
            Reglas aplicables.

    Returns:
        InsightRule:
            Regla seleccionada.
    """

    return max(
        rules,
        key=lambda rule: rule.priority,
    )


def _create_insight(cycle, rule):
    """
    Crea y almacena un insight.

    Si el ciclo ya posee un insight registrado,
    se devuelve el existente para evitar duplicados.

    Args:
        cycle:
            Ciclo analizado.

        rule:
            Regla seleccionada.

    Returns:
        Insight:
            Insight existente o recién creado.
    """

    existing_insight = Insight.objects.filter(
        user=cycle.user,
        cycle=cycle,
    ).first()

    if existing_insight is not None:
        return existing_insight

    return Insight.objects.create(
        user=cycle.user,
        cycle=cycle,
        phase=cycle.current_phase,
        type=rule.type,
        code=rule.code,
        title=rule.title,
        message=rule.message,
    )
