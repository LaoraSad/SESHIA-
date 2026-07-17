"""
Servicio encargado de la lógica de negocio relacionada con los registros diarios.

Responsibilities:
- Crear registros diarios.
- Actualizar registros diarios.
- Eliminar registros diarios.
- Consultar registros diarios según diferentes criterios.

Notes:
- Este módulo únicamente contiene lógica de negocio.
- No debe contener lógica de vistas, formularios o peticiones HTTP.
- Solo puede existir un registro diario por ciclo y por fecha.
"""
from datetime import date

from apps.cycles.models import Cycle, DailyLog, Symptom


def create_daily_log(
    cycle: Cycle,
    log_date: date,
    energy_level: int | None = None,
    mood: str | None = None,
    notes: str = "",
    symptoms: list[Symptom] | None = None,
) -> DailyLog:
    """
    Crea un registro diario para un ciclo menstrual.

    Args:
        cycle (Cycle):
            Ciclo al que pertenece el registro.

        log_date (date):
            Fecha correspondiente al registro.

        energy_level (int | None):
            Nivel de energía registrado por la usuaria.

        mood (str | None):
            Estado de ánimo registrado por la usuaria.

        notes (str):
            Notas adicionales del registro.

        symptoms (list[Symptom] | None):
            Lista de síntomas asociados al registro.

    Returns:
        DailyLog:
            Registro diario creado.

    Raises:
        ValueError:
            Si la fecha del registro no pertenece al ciclo.

    Notes:
        La fecha del registro debe encontrarse dentro del rango del
        ciclo menstrual. Los síntomas se asignan después de crear el
        registro debido a la relación ManyToMany.
    """

    if not (
        cycle.start_date <= log_date <= cycle.end_date
    ):
        raise ValueError(
            "La fecha del registro debe pertenecer al ciclo."
        )

    daily_log = DailyLog.objects.create(
        cycle=cycle,
        log_date=log_date,
        energy_level=energy_level,
        mood=mood,
        notes=notes,
    )

    if symptoms:
        daily_log.symptoms.set(symptoms)

    return daily_log

from cycles.models import DailyLog, Symptom

