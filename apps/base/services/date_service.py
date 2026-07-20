from datetime import date, timedelta

from apps.base.models import AppSettings


def get_current_date():
    settings = AppSettings.objects.first()
    if settings is not None:
        return settings.current_date
    return date.today()


def next_day():
    settings = AppSettings.objects.first()
    if settings is None:
        settings = AppSettings.objects.create(current_date=date.today())
    settings.current_date += timedelta(days=1)
    settings.save()
    return settings.current_date


def previous_day():
    settings = AppSettings.objects.first()
    if settings is None:
        settings = AppSettings.objects.create(current_date=date.today())
    settings.current_date -= timedelta(days=1)
    settings.save()
    return settings.current_date
