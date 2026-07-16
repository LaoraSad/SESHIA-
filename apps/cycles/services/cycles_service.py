from datetime import date

"""
Servicio encargado de la lógica de negocio relacionada con los ciclos menstruales.

Responsibilities:
- Registrar el inicio de un nuevo período menstrual.
- Crear nuevos ciclos menstruales.
- Finalizar automáticamente el ciclo anterior.
- Calcular la duración real del ciclo.
- Consultar ciclos según diferentes criterios.
- Consultar las fases de un ciclo según una fecha determinada.

Notes:
- Este módulo únicamente contiene lógica de negocio.
- No debe contener lógica de vistas, formularios o peticiones HTTP.
- Solo puede existir un ciclo activo por usuaria.
"""

def calculate_cycle_length(
    start_date: date,
    next_start_date: date,
    ) -> int:
    """
    Calcula la duración real de un ciclo menstrual.

    Args:
        start_date (date):
            Fecha de inicio del ciclo.

        next_start_date (date):
            Fecha de inicio del siguiente ciclo.

    Returns:
        int:
            Número de días transcurridos entre ambas fechas.

    Raises:
        ValueError:
            Si la fecha del siguiente ciclo no es posterior a la fecha de inicio.

    Notes:
        La duración del ciclo corresponde al número de días entre el
        primer día de una menstruación y el primer día de la siguiente.
    """
    if next_start_date <= start_date:
        raise ValueError(
            "La fecha del siguiente ciclo debe ser posterior a la fecha de inicio."
        )

    delta = next_start_date - start_date

    return delta.days

