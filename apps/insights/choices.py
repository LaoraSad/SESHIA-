from apps.base import models

class InsightType(models.TextChoices):

    FINANCE = "finance", "Finanzas"

    SYMPTOM = "symptom", "Síntomas"

    MOOD = "mood", "Estado de ánimo"

    ENERGY = "energy", "Energía"

    GENERAL = "general", "General"

