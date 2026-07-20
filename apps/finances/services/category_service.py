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

from django.db.models import Q, QuerySet

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

    name = name.strip()

    if not name:
        raise ValueError(
            "El nombre de la categoría no puede estar vacío."
        )

    if Category.objects.filter(
        user=user,
        category_type=category_type,
        name__iexact=name,
    ).exists():
        raise ValueError(
            f"Ya existe una categoría de tipo '{category_type}' con el nombre '{name}'."
        )

    return Category.objects.create(
        user=user,
        name=name,
        category_type=category_type,
        icon=icon,
        is_default=False,
        is_active=True,
    )


def update_category(
    category: Category,
    name: str,
    category_type: CategoryType,
    icon: str,
) -> Category:
    """
    Actualiza una categoría financiera personalizada.

    Args:
        category (Category):
            Categoría que será actualizada.

        name (str):
            Nuevo nombre de la categoría.

        category_type (CategoryType):
            Nuevo tipo de categoría.

        icon (str):
            Nuevo ícono de la categoría.

    Returns:
        Category:
            Categoría actualizada.

    Raises:
        ValueError:
            Si la categoría es una categoría predeterminada.

        ValueError:
            Si el nombre de la categoría está vacío.

    Notes:
        Las categorías predeterminadas son administradas por el
        sistema y no pueden modificarse.
    """

    if category.is_default:
        raise ValueError(
            "Las categorías predeterminadas no pueden modificarse."
        )

    if not name.strip():
        raise ValueError(
            "El nombre de la categoría no puede estar vacío."
        )

    new_name = name.strip()

    if Category.objects.filter(
        user=category.user,
        category_type=category_type,
        name__iexact=new_name,
    ).exclude(pk=category.pk).exists():
        raise ValueError(
            f"Ya existe una categoría de tipo '{category_type}' con el nombre '{new_name}'."
        )

    category.name = new_name
    category.category_type = category_type
    category.icon = icon

    category.save(
        update_fields=[
            "name",
            "category_type",
            "icon",
        ]
    )

    return category


def delete_category(
    category: Category,
) -> None:
    """
    Desactiva una categoría financiera personalizada.

    Args:
        category (Category):
            Categoría que será desactivada.

    Returns:
        None

    Raises:
        ValueError:
            Si la categoría es una categoría predeterminada.

    Notes:
        Las categorías predeterminadas son administradas por el
        sistema y no pueden desactivarse.

        La categoría no se elimina físicamente de la base de datos.
        Únicamente se marca como inactiva para conservar el historial
        de las transacciones asociadas.
    """

    if category.is_default:
        raise ValueError(
            "Las categorías predeterminadas no pueden desactivarse."
        )

    category.is_active = False

    category.save(
        update_fields=[
            "is_active",
        ]
    )


def get_category(
    user: User,
    category_id: int,
    ) -> Category | None:
    """
    Obtiene una categoría financiera disponible para una usuaria.

    Args:
        user (User):
            Usuaria que realiza la consulta.

        category_id (int):
            Identificador de la categoría.

    Returns:
        Category | None:
            Categoría encontrada o None si no existe.

    Notes:
        La búsqueda incluye tanto las categorías personalizadas de la
        usuaria como las categorías predeterminadas del sistema.
        Solo se consideran categorías activas.
    """

    return (
        Category.objects.filter(
            Q(user=user) | Q(is_default=True),
            id=category_id,
            is_active=True,
        )
        .first()
    )


def get_categories(
    user: User,
    ) -> QuerySet[Category]:
    """
    Obtiene todas las categorías financieras disponibles para una usuaria.

    Args:
        user (User):
            Usuaria que realiza la consulta.

    Returns:
        QuerySet[Category]:
            Conjunto de categorías disponibles para la usuaria.

    Notes:
        La consulta incluye las categorías predeterminadas del sistema
        y las categorías personalizadas de la usuaria.
        Solo se consideran categorías activas.
        Los resultados se devuelven utilizando el orden definido
        en el modelo.
    """

    return Category.objects.filter(
        Q(user=user) | Q(is_default=True),
        is_active=True,
    )

