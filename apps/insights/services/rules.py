"""
Catálogo de reglas utilizadas para generar insights personalizados.

Cada regla representa una posible recomendación que puede mostrarse
a una usuaria cuando se cumple una determinada condición.

Las condiciones asociadas a cada regla son evaluadas desde
`conditions.py`.

Notes:
    - Este módulo únicamente define el catálogo de reglas.
    - No contiene lógica de negocio.
    - No realiza consultas a la base de datos.
"""

from dataclasses import dataclass

from apps.insights.choices import InsightType, PhaseType


@dataclass(frozen=True)
class InsightRule:
    """
    Representa una regla utilizada para generar un insight.

    Cada regla define la información necesaria para construir
    una recomendación personalizada cuando una condición
    determinada es satisfecha.

    Attributes:
        code:
            Identificador único de la regla.

        type:
            Tipo de insight.

        phase:
            Fase del ciclo a la que pertenece la regla.
            Puede ser None cuando aplica de forma general.

        title:
            Título corto mostrado a la usuaria.

        message:
            Mensaje o recomendación que recibirá la usuaria.

        condition:
            Nombre de la función encargada de evaluar
            la condición desde conditions.py.

        priority:
            Prioridad utilizada para decidir qué insight
            mostrar cuando varias reglas son válidas.
    """

    code: str
    type: InsightType
    phase: PhaseType | None
    title: str
    message: str
    condition: str
    priority: int

CYCLE = InsightType.CYCLE
DAILY_LOG = InsightType.DAILY_LOG
FINANCE = InsightType.FINANCE
MIXED = InsightType.MIXED



CYCLE_RULES = [
    InsightRule(
        code="CYC001",
        type=CYCLE,
        phase=None,
        title="Ya podemos conocer mejor tu ciclo",
        message=(
            "Ya cuentas con varios ciclos registrados. "
            "Este historial permitirá identificar patrones "
            "y ofrecer recomendaciones cada vez más "
            "personalizadas."
        ),
        condition="has_enough_cycle_history",
        priority=1,
    ),
    InsightRule(
        code="CYC002",
        type=CYCLE,
        phase=None,
        title="Tus ciclos han sido consistentes",
        message=(
            "En tus últimos ciclos hemos observado una "
            "duración bastante constante. Mantener este "
            "registro facilita reconocer cambios importantes "
            "si llegan a presentarse."
        ),
        condition="stable_cycle_duration",
        priority=1,
    ),
    InsightRule(
        code="CYC003",
        type=CYCLE,
        phase=None,
        title="Detectamos cambios en tu ciclo",
        message=(
            "Hemos observado cambios en la duración de tus "
            "últimos ciclos. Continúa registrando tu "
            "información y, si esta tendencia se mantiene o "
            "te genera preocupación, considera consultar con "
            "un profesional de la salud."
        ),
        condition="variable_cycle_duration",
        priority=1,
    ),
    InsightRule(
        code="CYC004",
        type=CYCLE,
        phase=None,
        title="Sigamos construyendo tu historial",
        message=(
            "Aún estás construyendo tu historial menstrual. "
            "Registrar cada nuevo ciclo permitirá ofrecer "
            "recomendaciones más precisas y personalizadas."
        ),
        condition="insufficient_cycle_history",
        priority=1,
    ),
    InsightRule(
        code="CYC005",
        type=CYCLE,
        phase=None,
        title="Tu constancia hace la diferencia",
        message=(
            "Gracias a la información registrada durante "
            "varios ciclos, ahora es posible identificar "
            "tendencias con mayor confianza y generar "
            "recomendaciones más útiles."
        ),
        condition="has_extended_cycle_history",
        priority=1,
    ),
    InsightRule(
        code="CYC006",
        type=CYCLE,
        phase=None,
        title="Tu ciclo ha mantenido un patrón estable",
        message=(
            "Durante los últimos meses tu ciclo ha mostrado "
            "un comportamiento estable. Conocer tu patrón "
            "habitual facilita detectar cambios importantes "
            "cuando aparezcan."
        ),
        condition="stable_cycle_trend",
        priority=1,
    ),
    InsightRule(
        code="CYC007",
        type=CYCLE,
        phase=None,
        title="Observamos una nueva tendencia",
        message=(
            "En los últimos ciclos hemos identificado una "
            "tendencia en la duración de tu ciclo. Continúa "
            "registrando tu información para confirmar si "
            "este comportamiento se mantiene."
        ),
        condition="changing_cycle_trend",
        priority=1,
    ),
    InsightRule(
        code="CYC008",
        type=CYCLE,
        phase=None,
        title="Necesitamos un poco más de información",
        message=(
            "Aún no contamos con suficiente historial para "
            "identificar tendencias confiables. Sigue "
            "registrando tus ciclos para recibir "
            "recomendaciones más personalizadas."
        ),
        condition="not_enough_cycles_for_analysis",
        priority=1,
    ),
]


DAILY_LOG_RULES = [
    InsightRule(
        code="DAY001",
        type=DAILY_LOG,
        phase=None,
        title="Registraste poca energía en tu ciclo anterior",
        message=(
            "En tu ciclo anterior registraste niveles bajos "
            "de energía durante {phase}. Si este patrón se "
            "repite, considera organizar actividades exigentes "
            "en tus días de mayor energía."
        ),
        condition="previous_cycle_low_energy",
        priority=2,
    ),
    InsightRule(
        code="DAY002",
        type=DAILY_LOG,
        phase=PhaseType.OVULATORY,
        title="Esta suele ser una fase con buena energía",
        message=(
            "En ciclos anteriores registraste niveles altos "
            "de energía durante esta fase. Puede ser un buen "
            "momento para realizar actividades que requieran "
            "mayor esfuerzo físico o mental."
        ),
        condition="previous_cycle_high_energy",
        priority=2,
    ),
    InsightRule(
        code="DAY003",
        type=DAILY_LOG,
        phase=PhaseType.LUTEAL,
        title="Reconocimos un patrón en tu estado de ánimo",
        message=(
            "En varios ciclos registraste un estado de ánimo "
            "similar durante esta fase. Conocer estos patrones "
            "puede ayudarte a anticipar cómo podrías sentirte."
        ),
        condition="previous_cycle_mood_pattern",
        priority=2,
    ),
    InsightRule(
        code="DAY004",
        type=DAILY_LOG,
        phase=None,
        title="Un síntoma aparece con frecuencia",
        message=(
            "En ciclos anteriores registraste {value} con "
            "frecuencia. Llevar este seguimiento ayuda "
            "a reconocer mejor tus patrones personales."
        ),
        condition="previous_cycle_symptoms",
        priority=2,
    ),
    InsightRule(
        code="DAY005",
        type=DAILY_LOG,
        phase=None,
        title="Has registrado varios síntomas",
        message=(
            "En diferentes ciclos registraste varios síntomas "
            "durante un mismo periodo. Continuar registrándolos "
            "permitirá identificar patrones con mayor precisión."
        ),
        condition="multiple_previous_cycle_symptoms",
        priority=2,
    ),
    InsightRule(
        code="DAY006",
        type=DAILY_LOG,
        phase=None,
        title="Tu constancia está dando resultados",
        message=(
            "Gracias a la información que registras con "
            "frecuencia, la aplicación puede ofrecer "
            "recomendaciones cada vez más personalizadas."
        ),
        condition="consistent_daily_logs",
        priority=2,
    ),
    InsightRule(
        code="DAY007",
        type=DAILY_LOG,
        phase=None,
        title="Registra un poco más de tu día a día",
        message=(
            "Mientras más registros diarios completes, "
            "mejor podremos identificar patrones y generar "
            "recomendaciones adaptadas a tu ciclo."
        ),
        condition="insufficient_daily_logs",
        priority=1,
    ),
    InsightRule(
        code="DAY008",
        type=DAILY_LOG,
        phase=None,
        title="Tus anotaciones enriquecen tu historial",
        message=(
            "Las notas que registras complementan la "
            "información de tu ciclo y ayudan a comprender "
            "mejor situaciones que no pueden describirse "
            "solo con síntomas o estados de ánimo."
        ),
        condition="uses_notes_frequently",
        priority=2,
    ),
    InsightRule(
        code="DAY009",
        type=DAILY_LOG,
        phase=None,
        title="Llevas varios días con poca energía",
        message=(
            "Has registrado {value} días consecutivos con "
            "energía baja. Considera tomarlo con calma y "
            "descansar cuando lo necesites."
        ),
        condition="current_consecutive_low_energy",
        priority=3,
    ),
    InsightRule(
        code="DAY010",
        type=DAILY_LOG,
        phase=None,
        title="Tu estado de ánimo más frecuente",
        message=(
            "En lo que va del ciclo, tu estado de ánimo "
            "más frecuente ha sido {value}. Reconocer "
            "estos patrones te ayuda a conocerte mejor."
        ),
        condition="current_most_frequent_mood",
        priority=3,
    ),
    InsightRule(
        code="DAY011",
        type=DAILY_LOG,
        phase=None,
        title="Llevas {value} días registrando",
        message=(
            "Llevas {value} días seguidos registrando tu "
            "día a día. ¡Sigue así! Entre más información "
            "tengas, mejores serán las recomendaciones."
        ),
        condition="current_logging_streak",
        priority=3,
    ),
    InsightRule(
        code="DAY012",
        type=DAILY_LOG,
        phase=None,
        title="Un síntoma se repite en este ciclo",
        message=(
            "Has experimentado {value} en varios días de tu "
            "ciclo. Seguir registrándolo te ayudará a identificar "
            "patrones y comprender mejor cómo cambia tu cuerpo."
        ),
        condition="current_repeated_symptom",
        priority=3,
    ),
    InsightRule(
        code="DAY013",
        type=DAILY_LOG,
        phase=None,
        title="Llevas {value} días sin registrar tu día a día",
        message=(
            "Llevas {value} días sin registrar cómo te sientes. "
            "Registrar tu energía, estado de ánimo y síntomas "
            "ayuda a identificar patrones importantes en tu ciclo."
        ),
        condition="days_without_logging_streak",
        priority=5,
    ),
]


FINANCE_RULES = [
    # ── Prioridad 6: universales / temporales ────────────────────
    InsightRule(
        code="FIN007",
        type=FINANCE,
        phase=None,
        title="Empieza a registrar tus gastos",
        message=(
            "Aún no registras gastos en este ciclo. Llevar un "
            "control de tus finanzas te ayudará a identificar "
            "patrones según tu ciclo menstrual."
        ),
        condition="no_transactions_this_cycle",
        priority=6,
    ),
    InsightRule(
        code="FIN010",
        type=FINANCE,
        phase=None,
        title="Llevas {value} días sin registrar gastos",
        message=(
            "Llevas {value} días sin registrar movimientos "
            "financieros. Registrar tus gastos te permitirá "
            "tener una visión más completa de tu ciclo."
        ),
        condition="days_without_transactions_streak",
        priority=6,
    ),
    InsightRule(
        code="FIN001",
        type=FINANCE,
        phase=None,
        title="Tus gastos aumentaron",
        message=(
            "En este ciclo registraste un gasto mayor que en "
            "el ciclo anterior. Revisar este comportamiento "
            "puede ayudarte a identificar oportunidades de ahorro."
        ),
        condition="higher_total_expenses",
        priority=6,
    ),
    InsightRule(
        code="FIN002",
        type=FINANCE,
        phase=None,
        title="Lograste reducir tus gastos",
        message=(
            "En comparación con tu ciclo anterior, registraste "
            "un menor nivel de gastos. Mantener este hábito puede "
            "contribuir a una mejor planificación financiera."
        ),
        condition="lower_total_expenses",
        priority=6,
    ),
    # ── Prioridad 5: análisis del ciclo actual ───────────────────
    InsightRule(
        code="FIN008",
        type=FINANCE,
        phase=None,
        title="Conoce en qué fase gastas más",
        message=(
            "En lo que va del ciclo, la fase en la que más "
            "has gastado es {value}. Conocer este patrón puede "
            "ayudarte a planificar mejor tu presupuesto."
        ),
        condition="highest_spending_phase",
        priority=5,
    ),
    InsightRule(
        code="FIN009",
        type=FINANCE,
        phase=None,
        title="Tu categoría de gasto más frecuente",
        message=(
            "En este ciclo, tu categoría de gasto más recurrente "
            "ha sido {value}. Revisar estos hábitos te ayuda a "
            "tomar decisiones financieras más conscientes."
        ),
        condition="most_frequent_category",
        priority=5,
    ),
    InsightRule(
        code="FIN013",
        type=FINANCE,
        phase=None,
        title="Tus ingresos superan tus gastos",
        message=(
            "En este ciclo tus ingresos han sido mayores que "
            "tus gastos. Mantener este equilibrio es clave "
            "para una buena salud financiera."
        ),
        condition="income_exceeds_expenses",
        priority=5,
    ),
    InsightRule(
        code="FIN014",
        type=FINANCE,
        phase=None,
        title="Tus gastos superan tus ingresos",
        message=(
            "En este ciclo tus gastos han superado tus ingresos. "
            "Revisar tu presupuesto puede ayudarte a equilibrar "
            "tus finanzas."
        ),
        condition="expenses_exceed_income",
        priority=5,
    ),
    InsightRule(
        code="FIN011",
        type=FINANCE,
        phase=None,
        title="Tus gastos han aumentado",
        message=(
            "En los últimos 3 ciclos tus gastos han ido en "
            "aumento. Revisar esta tendencia puede ayudarte "
            "a identificar oportunidades de ahorro."
        ),
        condition="three_cycle_expense_increase",
        priority=5,
    ),
    InsightRule(
        code="FIN012",
        type=FINANCE,
        phase=None,
        title="Tus gastos se han reducido",
        message=(
            "En los últimos 3 ciclos has logrado reducir "
            "tus gastos. ¡Sigue así!"
        ),
        condition="three_cycle_expense_decrease",
        priority=5,
    ),
    InsightRule(
        code="FIN003",
        type=FINANCE,
        phase=PhaseType.MENSTRUAL,
        title="Sueles invertir más en tu bienestar",
        message=(
            "Durante esta fase has registrado con frecuencia "
            "gastos relacionados con tu bienestar personal. "
            "Planificarlos con anticipación puede ayudarte a "
            "administrar mejor tu presupuesto."
        ),
        condition="repeated_wellness_expenses",
        priority=5,
    ),
    InsightRule(
        code="FIN004",
        type=FINANCE,
        phase=PhaseType.LUTEAL,
        title="Tus gastos en alimentación aumentan en esta fase",
        message=(
            "En varios ciclos observamos un incremento en tus "
            "gastos de alimentación durante esta fase. Conocer "
            "este patrón puede ayudarte a planificar mejor tus compras."
        ),
        condition="repeated_food_expenses",
        priority=5,
    ),
    InsightRule(
        code="FIN005",
        type=FINANCE,
        phase=None,
        title="Tus gastos se mantienen estables",
        message=(
            "En los últimos ciclos tu nivel de gastos ha sido "
            "bastante consistente. Esto facilita una mejor "
            "planificación financiera."
        ),
        condition="stable_expense_pattern",
        priority=5,
    ),
    InsightRule(
        code="FIN006",
        type=FINANCE,
        phase=None,
        title="Registra más movimientos financieros",
        message=(
            "Mientras más transacciones registres, mejores "
            "recomendaciones podremos ofrecerte sobre tus hábitos "
            "financieros."
        ),
        condition="insufficient_transactions",
        priority=1,
    ),
]

MIXED_RULES = [
    InsightRule(
        code="MIX001",
        type=MIXED,
        phase=PhaseType.MENSTRUAL,
        title="Tus gastos aumentan cuando tienes menos energía",
        message=(
            "En ciclos anteriores registraste niveles bajos de "
            "energía y un aumento en determinados gastos durante "
            "esta fase. Anticipar este patrón puede ayudarte a "
            "planificar mejor tu presupuesto."
        ),
        condition="previous_cycle_low_energy_with_higher_expenses",
        priority=3,
    ),
    InsightRule(
        code="MIX002",
        type=MIXED,
        phase=PhaseType.LUTEAL,
        title="Tu estado de ánimo coincide con cambios en tus gastos",
        message=(
            "En varios ciclos observamos que los cambios en tu "
            "estado de ánimo durante esta fase coincidieron con "
            "variaciones en tus gastos. Conocer este patrón puede "
            "ayudarte a tomar decisiones más conscientes."
        ),
        condition="mood_related_expenses",
        priority=3,
    ),
    InsightRule(
        code="MIX003",
        type=MIXED,
        phase=PhaseType.MENSTRUAL,
        title="Los síntomas también influyen en tus gastos",
        message=(
            "Cuando registras determinados síntomas durante esta "
            "fase, también suele aumentar el gasto en categorías "
            "relacionadas con tu bienestar. Tenerlo presente puede "
            "facilitar una mejor planificación."
        ),
        condition="symptoms_related_expenses",
        priority=3,
    ),
    InsightRule(
        code="MIX004",
        type=MIXED,
        phase=PhaseType.OVULATORY,
        title="Aprovechas tu fase de mayor energía",
        message=(
            "En ciclos anteriores registraste niveles altos de "
            "energía y mantuviste un comportamiento financiero "
            "estable durante esta fase. Continúa aprovechando este "
            "momento para organizar actividades importantes."
        ),
        condition="high_energy_with_stable_expenses",
        priority=3,
    ),
    InsightRule(
        code="MIX006",
        type=MIXED,
        phase=None,
        title="Tu información está generando recomendaciones más útiles",
        message=(
            "La combinación de los registros de tu ciclo, tus "
            "anotaciones diarias y tus transacciones permite ofrecer "
            "recomendaciones cada vez más personalizadas."
        ),
        condition="enough_data_for_mixed_analysis",
        priority=1,
    ),
    InsightRule(
        code="MIX007",
        type=MIXED,
        phase=None,
        title="Tu energía baja influye en tus gastos",
        message=(
            "En los días con poca energía, tus gastos se concentran "
            "en {value}. Conocer esta relación puede ayudarte a "
            "tomar decisiones más conscientes."
        ),
        condition="low_energy_with_category",
        priority=3,
    ),
    InsightRule(
        code="MIX008",
        type=MIXED,
        phase=None,
        title="Tu estado de ánimo y tus gastos están conectados",
        message=(
            "Cuando tu estado de ánimo es {mood}, sueles gastar "
            "en {category}. Identificar estos patrones te ayuda "
            "a planificar mejor tu presupuesto."
        ),
        condition="mood_with_category",
        priority=3,
    ),
]

ALL_RULES: list[InsightRule] = [
    *CYCLE_RULES,
    *DAILY_LOG_RULES,
    *FINANCE_RULES,
    *MIXED_RULES,
]
