"""
Servicios encargados de generar y consultar insights.

Responsibilities:
    - Generar insights personalizados.
    - Evaluar las reglas disponibles.
    - Seleccionar el insight más relevante.
    - Almacenar el historial de insights.
"""
from django.db.models import QuerySet

from apps.cycles.models.phase import Phase
from apps.insights.choices import InsightType
from apps.insights.models import Insight
from apps.insights.services.conditions import CONDITIONS
from apps.insights.services.rules import ALL_RULES
from apps.users.models import User


def generate_insight(cycle):
    applicable = _get_applicable_rules(cycle)

    if not applicable:
        return None

    rule, context = _select_best_rule(applicable)

    return _create_insight(cycle, rule, context)


def _get_applicable_rules(cycle):
    applicable = []

    for rule in ALL_RULES:
        condition_func = CONDITIONS.get(rule.condition)

        if condition_func is None:
            continue

        if rule.type == InsightType.CYCLE:
            result = condition_func(cycle.user)
        else:
            result = condition_func(cycle)

        if result:
            applicable.append((rule, result))

    return applicable


def _select_best_rule(rules):
    return max(
        rules,
        key=lambda item: item[0].priority,
    )


def _resolve_insight_phase(cycle, rule):
    """Determina la fase del ciclo que debe asociarse al insight.

    Usa la fase indicada por la regla si existe y está presente
    en el ciclo; de lo contrario usa la fase actual del ciclo;
    si todo falla, usa la primera fase del ciclo.
    """
    if rule.phase is not None:
        phase_name = rule.phase.label
        cycle_phase = cycle.phases.filter(
            phase__name__iexact=phase_name,
        ).first()
        if cycle_phase is not None:
            return cycle_phase.phase

    current = cycle.current_phase
    if current is not None:
        return current

    first = cycle.phases.first()
    if first is not None:
        return first.phase

    return None


def _create_insight(cycle, rule, context=None):
    existing_insight = Insight.objects.filter(
        user=cycle.user,
        cycle=cycle,
    ).first()

    if existing_insight is not None:
        return existing_insight

    phase = _resolve_insight_phase(cycle, rule)

    if phase is None:
        return None

    message = rule.message
    if context and isinstance(context, str):
        message = message.replace("{value}", context)
        message = message.replace("{phase}", context)

    return Insight.objects.create(
        user=cycle.user,
        cycle=cycle,
        phase=phase,
        type=rule.type,
        code=rule.code,
        title=rule.title,
        message=message,
    )


def get_latest_insight(
    user: User,
) -> Insight | None:
    return Insight.objects.filter(
        user=user,
    ).first()


def get_insight_history(
    user: User,
) -> QuerySet[Insight]:
    return Insight.objects.filter(
        user=user,
    )