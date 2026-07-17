"""
Servicio encargado de la lógica de negocio relacionada con los insights.

Responsibilities:
- Generar insights para una usuaria.
- Obtener el insight más reciente.
- Consultar el historial de insights.

Notes:
- Este módulo únicamente contiene lógica de negocio.
- No debe contener lógica de vistas, formularios o peticiones HTTP.
- Los insights se generan utilizando la información disponible del ciclo
  menstrual y las transacciones de la usuaria.
"""
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

    


