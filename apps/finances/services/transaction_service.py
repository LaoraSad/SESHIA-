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

from apps.cycles.services.cycles_service import get_cycle_by_date, get_cycle_phase_by_date
from apps.finances.models import Category, Transaction
from apps.users.models import User
from apps.cycles.services.cycles_service import (get_cycle_by_date, get_cycle_phase_by_date)



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

