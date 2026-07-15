from django.db import models


class CategoryType(models.TextChoices):
    """
    Tipos de categorías disponibles para clasificar transacciones.
    """

    INCOME = "income", "Ingreso"
    EXPENSE = "expense", "Gasto"



