"""
Servicio encargado de la lógica de negocio relacionada con las categorías financieras.

Responsibilities:
- Crear categorías personalizadas.
- Actualizar categorías existentes.
- Eliminar categorías personalizadas.
- Consultar categorías disponibles para una usuaria.

Notes:
- Este módulo únicamente contiene lógica de negocio.
- No debe contener lógica de vistas, formularios o peticiones HTTP.
- Las categorías predeterminadas son administradas por el sistema.
"""

from apps.finances.choices import CategoryType
from apps.finances.models import Category
from apps.users.models import User


def create_category(
    user: User,
    name: str,
    category_type: CategoryType,
    icon: str,
    ) -> Category:
    """
    Crea una nueva categoría financiera personalizada.

    Args:
        user (User):
            Usuaria propietaria de la categoría.

        name (str):
            Nombre de la categoría.

        category_type (CategoryType):
            Tipo de categoría (ingreso o gasto).

        icon (str):
            Ícono representativo de la categoría.

    Returns:
        Category:
            Categoría creada.

    Raises:
        ValueError:
            Si el nombre de la categoría está vacío.

    Notes:
        Las categorías creadas mediante este servicio siempre son
        categorías personalizadas, por lo que se asocian a la
        usuaria y el campo ``is_default`` se establece
        automáticamente en ``False``.
    """

    if not name.strip():
        raise ValueError(
            "El nombre de la categoría no puede estar vacío."
        )

    return Category.objects.create(
        user=user,
        name=name.strip(),
        category_type=category_type,
        icon=icon,
        is_default=False,
        is_active=True,
    )