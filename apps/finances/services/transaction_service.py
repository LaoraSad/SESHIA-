"""
Servicio encargado de la lógica de negocio relacionada con las transacciones financieras.

Responsibilities:
- Crear transacciones financieras.
- Actualizar transacciones existentes.
- Eliminar transacciones.
- Consultar transacciones según diferentes criterios.
- Asociar automáticamente las transacciones al ciclo menstrual y a la fase correspondiente.

Notes:
- Este módulo únicamente contiene lógica de negocio.
- No debe contener lógica de vistas, formularios o peticiones HTTP.
- Cada transacción pertenece a una única usuaria.
"""
from datetime import date
from decimal import Decimal

from django.db.models import QuerySet

from apps.cycles.services.cycles_service import get_cycle_by_date, get_cycle_phase_by_date
from apps.finances.models import Category, Transaction
from apps.users.models import User


def create_transaction(
    user: User,
    category: Category,
    amount: Decimal,
    transaction_date: date,
    description: str = "",
) -> Transaction:
    """
    Crea una nueva transacción financiera.

    Args:
        user (User):
            Usuaria propietaria de la transacción.

        category (Category):
            Categoría asociada a la transacción.

        amount (Decimal):
            Monto de la transacción.

        transaction_date (date):
            Fecha en la que se realizó la transacción.

        description (str):
            Descripción opcional de la transacción.

    Returns:
        Transaction:
            Transacción creada.

    Raises:
        ValueError:
            Si el monto es menor o igual a cero.

        ValueError:
            Si no existe un ciclo para la fecha indicada.

        ValueError:
            Si no existe una fase del ciclo para la fecha indicada.

    Notes:
        El ciclo menstrual y la fase del ciclo se determinan
        automáticamente a partir de la fecha de la transacción.
    """

    if amount <= Decimal("0"):
        raise ValueError(
            "El monto debe ser mayor que cero."
        )

    cycle = get_cycle_by_date(
        user=user,
        target_date=transaction_date,
    )

    if cycle is None:
        raise ValueError(
            "No existe un ciclo menstrual para la fecha indicada."
        )

    cycle_phase = get_cycle_phase_by_date(
        cycle=cycle,
        target_date=transaction_date,
    )

    if cycle_phase is None:
        raise ValueError(
            "No existe una fase del ciclo para la fecha indicada."
        )

    return Transaction.objects.create(
        user=user,
        category=category,
        cycle=cycle,
        cycle_phase=cycle_phase,
        amount=amount,
        transaction_date=transaction_date,
        description=description,
    )


def update_transaction(
    transaction: Transaction,
    category: Category,
    amount: Decimal,
    transaction_date: date,
    description: str = "",
) -> Transaction:
    """
    Actualiza una transacción financiera.

    Args:
        transaction (Transaction):
            Transacción que será actualizada.

        category (Category):
            Nueva categoría de la transacción.

        amount (Decimal):
            Nuevo monto de la transacción.

        transaction_date (date):
            Nueva fecha de la transacción.

        description (str):
            Nueva descripción de la transacción.

    Returns:
        Transaction:
            Transacción actualizada.

    Raises:
        ValueError:
            Si el monto es menor o igual a cero.

        ValueError:
            Si no existe un ciclo para la fecha indicada.

        ValueError:
            Si no existe una fase del ciclo para la fecha indicada.

    Notes:
        Si la fecha de la transacción cambia, el ciclo menstrual y la
        fase del ciclo se recalculan automáticamente.
    """

    if amount <= Decimal("0"):
        raise ValueError(
            "El monto debe ser mayor que cero."
        )

    cycle = get_cycle_by_date(
        user=transaction.user,
        target_date=transaction_date,
    )

    if cycle is None:
        raise ValueError(
            "No existe un ciclo menstrual para la fecha indicada."
        )

    cycle_phase = get_cycle_phase_by_date(
        cycle=cycle,
        target_date=transaction_date,
    )

    if cycle_phase is None:
        raise ValueError(
            "No existe una fase del ciclo para la fecha indicada."
        )

    transaction.category = category
    transaction.amount = amount
    transaction.transaction_date = transaction_date
    transaction.description = description
    transaction.cycle = cycle
    transaction.cycle_phase = cycle_phase

    transaction.save(
        update_fields=[
            "category",
            "amount",
            "transaction_date",
            "description",
            "cycle",
            "cycle_phase",
        ]
    )

    return transaction


def delete_transaction(
    transaction: Transaction,
) -> None:
    """
    Desactiva una transacción financiera (soft delete).

    La transacción permanece en la base de datos con is_active=False
    para no afectar los cálculos de insights históricos.

    Args:
        transaction (Transaction):
            Transacción que será desactivada.

    Returns:
        None
    """

    transaction.is_active = False

    transaction.save(
        update_fields=[
            "is_active",
        ]
    )


def get_transaction(
    user: User,
    transaction_id: int,
) -> Transaction | None:
    """
    Obtiene una transacción financiera de una usuaria.

    Args:
        user (User):
            Usuaria propietaria de la transacción.

        transaction_id (int):
            Identificador de la transacción.

    Returns:
        Transaction | None:
            Transacción encontrada o None si no existe.

    Notes:
        La búsqueda se realiza únicamente entre las
        transacciones de la usuaria.
    """

    return Transaction.objects.filter(
        user=user,
        id=transaction_id,
        is_active=True,
    ).first()


def get_transactions(
    user: User,
) -> QuerySet[Transaction]:
    """
    Obtiene todas las transacciones financieras de una usuaria.

    Args:
        user (User):
            Usuaria propietaria de las transacciones.

    Returns:
        QuerySet[Transaction]:
            Conjunto de transacciones pertenecientes a la usuaria.

    Notes:
        Las transacciones se devuelven utilizando el orden definido
        en el modelo.
    """

    return Transaction.objects.filter(
        user=user,
        is_active=True,
    )

def get_transactions_by_category(
    user: User,
    category: Category,
) -> QuerySet[Transaction]:
    """
    Obtiene las transacciones financieras de una usuaria
    pertenecientes a una categoría determinada.

    Args:
        user (User):
            Usuaria propietaria de las transacciones.

        category (Category):
            Categoría utilizada para filtrar las transacciones.

    Returns:
        QuerySet[Transaction]:
            Conjunto de transacciones que pertenecen a la categoría
            indicada.

    Notes:
        Las transacciones se devuelven utilizando el orden definido
        en el modelo.
    """

    return Transaction.objects.filter(
        user=user,
        category=category,
    )


def get_transactions_by_date_range(
    user: User,
    start_date: date,
    end_date: date,
) -> QuerySet[Transaction]:
    """
    Obtiene las transacciones financieras de una usuaria
    comprendidas entre dos fechas.

    Args:
        user (User):
            Usuaria propietaria de las transacciones.

        start_date (date):
            Fecha inicial del rango.

        end_date (date):
            Fecha final del rango.

    Returns:
        QuerySet[Transaction]:
            Conjunto de transacciones comprendidas
            entre las fechas indicadas.

    Raises:
        ValueError:
            Si la fecha final es anterior a la fecha inicial.

    Notes:
        Las transacciones se devuelven utilizando el orden
        definido en el modelo.
    """

    if end_date < start_date:
        raise ValueError(
            "La fecha final debe ser igual o posterior a la fecha inicial."
        )

    return Transaction.objects.filter(
        user=user,
        transaction_date__range=(
            start_date,
            end_date,
        ),
    )
