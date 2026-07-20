from apps.base.services.date_service import get_current_date


def current_date(request):
    return {"current_date": get_current_date()}
