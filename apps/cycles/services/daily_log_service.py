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

from django.db.models import QuerySet

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


def update_daily_log(
    daily_log: DailyLog,
    energy_level: int | None = None,
    mood: str | None = None,
    notes: str = "",
    symptoms: list[Symptom] | None = None,
) -> DailyLog:
    """
    Actualiza la información de un registro diario.

    Args:
        daily_log (DailyLog):
            Registro diario que será actualizado.

        energy_level (int | None):
            Nuevo nivel de energía registrado.

        mood (str | None):
            Nuevo estado de ánimo registrado.

        notes (str):
            Nuevas notas asociadas al registro.

        symptoms (list[Symptom] | None):
            Nueva lista de síntomas asociados al registro.

    Returns:
        DailyLog:
            Registro diario actualizado.

    Notes:
        Este servicio únicamente permite modificar la información
        registrada por la usuaria. El ciclo y la fecha del registro
        permanecen inalterables para conservar la integridad de los
        datos.
    """

    daily_log.energy_level = energy_level
    daily_log.mood = mood
    daily_log.notes = notes

    daily_log.save(
        update_fields=[
            "energy_level",
            "mood",
            "notes",
        ]
    )

    daily_log.symptoms.set(symptoms or [])

    return daily_log


def delete_daily_log(
    daily_log: DailyLog,
) -> None:
    """
    Elimina un registro diario.

    Args:
        daily_log (DailyLog):
            Registro diario que será eliminado.

    Returns:
        None

    Notes:
        El registro se elimina de forma permanente de la base de datos.
        Este servicio debe utilizarse cuando la usuaria desee eliminar
        un registro creado por error.
    """

    daily_log.delete()


def get_daily_log_by_date(
    cycle: Cycle,
    log_date: date,
) -> DailyLog | None:
    """
    Obtiene el registro diario correspondiente a una fecha de un ciclo.

    Args:
        cycle (Cycle):
            Ciclo al que pertenece el registro.

        log_date (date):
            Fecha del registro.

    Returns:
        DailyLog | None:
            Registro diario encontrado o None si no existe.

    Notes:
        La búsqueda se realiza utilizando el ciclo y la fecha del
        registro. Solo puede existir un registro por día dentro de
        un mismo ciclo.
    """

    return (
        DailyLog.objects.filter(
            cycle=cycle,
            log_date=log_date,
        )
        .first()
    )


def get_daily_logs_by_cycle(
    cycle: Cycle,
    ) -> QuerySet[DailyLog]:
    """
    Obtiene todos los registros diarios pertenecientes a un ciclo menstrual.

    Args:
        cycle (Cycle):
            Ciclo cuyos registros diarios serán consultados.

    Returns:
        QuerySet[DailyLog]:
            Conjunto de registros diarios pertenecientes al ciclo.

    Notes:
        Los registros se devuelven utilizando el orden definido en el
        modelo.
    """

    return DailyLog.objects.filter(
        cycle=cycle,
    )

