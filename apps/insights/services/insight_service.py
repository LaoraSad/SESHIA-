"""
Servicios encargados de generar y consultar insights.

Responsibilities:
    - Generar insights personalizados.
    - Evaluar las reglas disponibles.
    - Seleccionar el insight más relevante.
    - Almacenar el historial de insights.
"""
from django.db.models import QuerySet

from apps.base.services.date_service import get_current_date
from apps.cycles.models.phase import Phase
from apps.insights.choices import InsightType
from apps.insights.models import Insight
from apps.insights.services.conditions import CONDITIONS
from apps.insights.services.rules import ALL_RULES
from apps.users.models import User


def generate_insight(cycle):
    current = Insight.objects.filter(
        user=cycle.user,
        cycle=cycle,
    ).first()

    if current is not None:
        today = get_current_date()
        last_date = current.shown_at.date()

        if today == last_date:
            has_new = (
                cycle.daily_logs.filter(
                    log_date__gte=current.shown_at,
                ).exists()
                or cycle.transactions.filter(
                    is_active=True,
                    transaction_date__gte=current.shown_at.date(),
                ).exists()
            )
            if not has_new:
                return current

    applicable = _get_applicable_rules(cycle)

    if not applicable:
        return current

    # Última acción del usuario en el ciclo
    last_log = cycle.daily_logs.order_by("-log_date").first()
    last_tx = (
        cycle.transactions.filter(is_active=True)
        .order_by("-transaction_date")
        .first()
    )

    last_is_log = last_log is not None and (
        last_tx is None or last_log.log_date >= last_tx.transaction_date
    )
    last_is_tx = last_tx is not None and (
        last_log is None or last_tx.transaction_date > last_log.log_date
    )

    if last_is_log:
        group = [r for r in applicable if r[0].type != InsightType.FINANCE]
    elif last_is_tx:
        group = [r for r in applicable if r[0].type == InsightType.FINANCE]
    else:
        group = []

    if group:
        current_code = current.code if current else None
        otras = [r for r in group if r[0].code != current_code]
        applicable = otras or group

    rule, context = _select_best_rule(applicable)

    if current is not None and current.code == rule.code:
        return current

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
    """Siempre usa la fase actual del ciclo como etiqueta del insight."""
    current = cycle.current_phase
    if current is not None:
        return current

    first = cycle.phases.first()
    if first is not None:
        return first.phase

    return None


def _create_insight(cycle, rule, context=None):
    phase = _resolve_insight_phase(cycle, rule)

    if phase is None:
        return None

    title = rule.title
    message = rule.message
    if context:
        if isinstance(context, str):
            title = title.replace("{value}", context)
            title = title.replace("{phase}", context)
            message = message.replace("{value}", context)
            message = message.replace("{phase}", context)
        elif isinstance(context, dict):
            for key, val in context.items():
                title = title.replace("{" + key + "}", str(val))
                message = message.replace("{" + key + "}", str(val))

    return Insight.objects.create(
        user=cycle.user,
        cycle=cycle,
        phase=phase,
        type=rule.type,
        code=rule.code,
        title=title,
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