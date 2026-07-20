from datetime import date

from django.db import migrations


def seed_app_settings(apps, schema_editor):
    AppSettings = apps.get_model("base", "AppSettings")
    AppSettings.objects.create(current_date=date.today())


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_app_settings, migrations.RunPython.noop),
    ]
