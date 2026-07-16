from django.db import models


class EnergyLevel(models.IntegerChoices):
    """
    Niveles de energía disponibles para el registro diario.
    """

    VERY_LOW = 1, "Muy baja"
    LOW = 2, "Baja"
    NORMAL = 3, "Normal"
    HIGH = 4, "Alta"
    VERY_HIGH = 5, "Muy alta"


class Mood(models.TextChoices):
    """
    Estados de ánimo disponibles para el registro diario.
    """

    HAPPY = "happy", "😊 Feliz"
    CALM = "calm", "😌 Tranquila"
    NEUTRAL = "neutral", "😐 Neutral"
    SAD = "sad", "😔 Triste"
    IRRITABLE = "irritable", "😠 Irritable"
    ANXIOUS = "anxious", "😰 Ansiosa"

class CycleStatus(models.TextChoices):
    """
    Estados posibles de un ciclo menstrual.
    """

    ACTIVE = "ACTIVE", "Activo"
    COMPLETED = "COMPLETED", "Completado"

