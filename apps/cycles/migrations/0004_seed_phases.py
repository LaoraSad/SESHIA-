from django.db import migrations


def load_phases(apps, schema_editor):
    Phase = apps.get_model("cycles", "Phase")

    phases = [
        {
            "name": "Menstrual",
            "description": "Comienza el primer día del período menstrual. Durante esta fase, el útero se desprende de su revestimiento, lo que produce el sangrado menstrual.",
            "estimated_percentage": 18.00,
            "sort_order": 1,
        },
        {
            "name": "Folicular",
            "description": "Comienza después de la menstruación. Las hormonas estimulan el crecimiento de los folículos en los ovarios.",
            "estimated_percentage": 32.00,
            "sort_order": 2,
        },
        {
            "name": "Ovulatoria",
            "description": "Ocurre cuando un óvulo maduro es liberado del ovario. Es el período más fértil del ciclo.",
            "estimated_percentage": 11.00,
            "sort_order": 3,
        },
        {
            "name": "Lútea",
            "description": "Comienza después de la ovulación. El cuerpo se prepara para un posible embarazo.",
            "estimated_percentage": 39.00,
            "sort_order": 4,
        },
    ]

    for phase_data in phases:
        Phase.objects.create(**phase_data)


def reverse_load_phases(apps, schema_editor):
    Phase = apps.get_model("cycles", "Phase")
    Phase.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("cycles", "0003_load_symptoms"),
    ]

    operations = [
        migrations.RunPython(
            load_phases,
            reverse_load_phases,
        ),
    ]
