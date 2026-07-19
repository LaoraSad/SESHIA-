from django.db import models

class InsightType(models.TextChoices):

    CYCLE = "cycle", "Ciclo"

    DAILY_LOG = "daily_log", "Registro diario"

    FINANCE = "finance", "Finanzas"

    MIXED = "mixed", "Mixto"

    SYMPTOM = "symptom", "Síntomas"

    MOOD = "mood", "Estado de ánimo"

    ENERGY = "energy", "Energía"

    GENERAL = "general", "General"



class PhaseType(models.TextChoices):
    """
    Fases del ciclo menstrual utilizadas por las reglas de insights.
    """

    MENSTRUAL = "menstrual", "Menstrual"
    FOLLICULAR = "folicular", "Folicular"
    OVULATORY = "ovulatoria", "Ovulatoria"
    LUTEAL = "lútea", "Lútea"
