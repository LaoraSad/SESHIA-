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

from apps.cycles.choices import PhaseType
from apps.insights.choices import InsightType


CYCLE_RULES = [
    {
        "code": "CYC001",
        "type": InsightType.CYCLE,
        "phase": None,
        "title": "Ya podemos conocer mejor tu ciclo",
        "message": (
            "Ya cuentas con varios ciclos registrados. "
            "Este historial permitirá identificar patrones "
            "y ofrecer recomendaciones cada vez más "
            "personalizadas."
        ),
        "condition": "has_enough_cycle_history",
        "priority": 5,
    },
    {
        "code": "CYC002",
        "type": InsightType.CYCLE,
        "phase": None,
        "title": "Tus ciclos han sido consistentes",
        "message": (
            "En tus últimos ciclos hemos observado una "
            "duración bastante constante. Mantener este "
            "registro facilita reconocer cambios importantes "
            "si llegan a presentarse."
        ),
        "condition": "stable_cycle_duration",
        "priority": 4,
    },
    {
        "code": "CYC003",
        "type": InsightType.CYCLE,
        "phase": None,
        "title": "Detectamos cambios en tu ciclo",
        "message": (
            "Hemos observado cambios en la duración de tus "
            "últimos ciclos. Continúa registrando tu "
            "información y, si esta tendencia se mantiene o "
            "te genera preocupación, considera consultar con "
            "un profesional de la salud."
        ),
        "condition": "variable_cycle_duration",
        "priority": 2,
    },
    {
        "code": "CYC004",
        "type": InsightType.CYCLE,
        "phase": None,
        "title": "Sigamos construyendo tu historial",
        "message": (
            "Aún estás construyendo tu historial menstrual. "
            "Registrar cada nuevo ciclo permitirá ofrecer "
            "recomendaciones más precisas y personalizadas."
        ),
        "condition": "insufficient_cycle_history",
        "priority": 6,
    },
    {
        "code": "CYC005",
        "type": InsightType.CYCLE,
        "phase": None,
        "title": "Tu constancia hace la diferencia",
        "message": (
            "Gracias a la información registrada durante "
            "varios ciclos, ahora es posible identificar "
            "tendencias con mayor confianza y generar "
            "recomendaciones más útiles."
        ),
        "condition": "has_extended_cycle_history",
        "priority": 5,
    },
    {
        "code": "CYC006",
        "type": InsightType.CYCLE,
        "phase": None,
        "title": "Tu ciclo ha mantenido un patrón estable",
        "message": (
            "Durante los últimos meses tu ciclo ha mostrado "
            "un comportamiento estable. Conocer tu patrón "
            "habitual facilita detectar cambios importantes "
            "cuando aparezcan."
        ),
        "condition": "stable_cycle_trend",
        "priority": 4,
    },
    {
        "code": "CYC007",
        "type": InsightType.CYCLE,
        "phase": None,
        "title": "Observamos una nueva tendencia",
        "message": (
            "En los últimos ciclos hemos identificado una "
            "tendencia en la duración de tu ciclo. Continúa "
            "registrando tu información para confirmar si "
            "este comportamiento se mantiene."
        ),
        "condition": "changing_cycle_trend",
        "priority": 3,
    },
    {
        "code": "CYC008",
        "type": InsightType.CYCLE,
        "phase": None,
        "title": "Necesitamos un poco más de información",
        "message": (
            "Aún no contamos con suficiente historial para "
            "identificar tendencias confiables. Sigue "
            "registrando tus ciclos para recibir "
            "recomendaciones más personalizadas."
        ),
        "condition": "not_enough_cycles_for_analysis",
        "priority": 6,
    },
]

DAILY_LOG_RULES = [
    {
        "code": "DAY001",
        "type": InsightType.DAILY_LOG,
        "phase": None,
        "title": "Has registrado niveles bajos de energía",
        "message": (
            "En varios ciclos has registrado niveles bajos de "
            "energía durante esta fase. Si este patrón continúa, "
            "podría ayudarte planificar actividades exigentes en "
            "momentos donde normalmente te sientas con más energía."
        ),
        "condition": "repeated_low_energy",
        "priority": 2,
    },
    {
        "code": "DAY002",
        "type": InsightType.DAILY_LOG,
        "phase": None,
        "title": "Has registrado buena energía",
        "message": (
            "En varios ciclos has registrado niveles altos de "
            "energía durante esta fase. Puede ser un buen momento "
            "para planificar actividades que requieran mayor esfuerzo."
        ),
        "condition": "repeated_high_energy",
        "priority": 5,
    },
    {
        "code": "DAY003",
        "type": InsightType.DAILY_LOG,
        "phase": None,
        "title": "Observamos un patrón en tu estado de ánimo",
        "message": (
            "Durante varios ciclos has registrado un estado de "
            "ánimo similar en esta fase. Conocer estos patrones "
            "puede ayudarte a organizar mejor tus actividades y "
            "anticipar cómo podrías sentirte."
        ),
        "condition": "repeated_mood_pattern",
        "priority": 3,
    },
    {
        "code": "DAY004",
        "type": InsightType.DAILY_LOG,
        "phase": None,
        "title": "Un síntoma aparece con frecuencia",
        "message": (
            "Hemos observado que uno de tus síntomas se repite "
            "en varios ciclos durante esta fase. Llevar este "
            "registro puede ayudarte a reconocer mejor tus "
            "patrones personales."
        ),
        "condition": "repeated_symptom",
        "priority": 2,
    },
    {
        "code": "DAY005",
        "type": InsightType.DAILY_LOG,
        "phase": None,
        "title": "Has registrado varios síntomas",
        "message": (
            "En esta fase has registrado varios síntomas de "
            "forma repetida. Continúa registrando esta "
            "información para conocer mejor la evolución de "
            "tu ciclo."
        ),
        "condition": "multiple_repeated_symptoms",
        "priority": 2,
    },
    {
        "code": "DAY006",
        "type": InsightType.DAILY_LOG,
        "phase": None,
        "title": "Tu registro diario está dando resultados",
        "message": (
            "Gracias a la constancia con la que registras tu "
            "información diaria, la aplicación puede detectar "
            "patrones con mayor precisión."
        ),
        "condition": "consistent_daily_logs",
        "priority": 5,
    },
    {
        "code": "DAY007",
        "type": InsightType.DAILY_LOG,
        "phase": None,
        "title": "Registra más información diaria",
        "message": (
            "Mientras más registros diarios completes, más "
            "precisas podrán ser las recomendaciones que "
            "recibas en el futuro."
        ),
        "condition": "insufficient_daily_logs",
        "priority": 6,
    },
    {
        "code": "DAY008",
        "type": InsightType.DAILY_LOG,
        "phase": None,
        "title": "Tus anotaciones complementan el seguimiento",
        "message": (
            "Las notas que registras ayudan a complementar la "
            "información de tu ciclo y facilitan recordar "
            "situaciones importantes en el futuro."
        ),
        "condition": "uses_notes_frequently",
        "priority": 5,
    },
]
