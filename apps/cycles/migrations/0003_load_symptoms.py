from django.db import migrations


def load_symptoms(apps, schema_editor):
    SymptomCategory = apps.get_model("cycles", "SymptomCategory")
    Symptom = apps.get_model("cycles", "Symptom")

    categories = [
        {
            "name": "Dolor",
            "icon": "🤕",
            "description": "Síntomas relacionados con dolor.",
            "sort_order": 1,
            "symptoms": [
                "Cólicos",
                "Dolor abdominal",
                "Dolor lumbar",
                "Dolor de cabeza",
                "Dolor en los senos",
            ],
        },
        {
            "name": "Digestivo",
            "icon": "🍽️",
            "description": "Síntomas digestivos.",
            "sort_order": 2,
            "symptoms": [
                "Náuseas",
                "Hinchazón",
                "Estreñimiento",
                "Diarrea",
            ],
        },
        {
            "name": "Flujo",
            "icon": "💧",
            "description": "Cambios en el flujo vaginal.",
            "sort_order": 3,
            "symptoms": [
                "Flujo abundante",
                "Flujo ligero",
                
            ],
        },
        {
            "name": "Piel",
            "icon": "🌸",
            "description": "Cambios en la piel.",
            "sort_order": 4,
            "symptoms": [
                "Acné",
                "Piel grasa",
            ],
        },
        {
            "name": "Sueño",
            "icon": "😴",
            "description": "Alteraciones del sueño.",
            "sort_order": 5,
            "symptoms": [
                "Insomnio",
                "Somnolencia",
                "Fatiga",
            ],
        },
        {
            "name": "Antojos",
            "icon": "🍫",
            "description": "Cambios en el apetito.",
            "sort_order": 6,
            "symptoms": [
                "Antojos",
                "Aumento del apetito",
                "Pérdida del apetito",
            ],
        },
    ]

    symptom_order = 1

    for category_data in categories:
        category = SymptomCategory.objects.create(
            name=category_data["name"],
            icon=category_data["icon"],
            description=category_data["description"],
            sort_order=category_data["sort_order"],
        )

        for symptom_name in category_data["symptoms"]:
            Symptom.objects.create(
                category=category,
                name=symptom_name,
                sort_order=symptom_order,
            )

            symptom_order += 1


def reverse_load_symptoms(apps, schema_editor):
    SymptomCategory = apps.get_model("cycles", "SymptomCategory")

    SymptomCategory.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("cycles", "0002_initial"),
    ]

    operations = [
        migrations.RunPython(
            load_symptoms,
            reverse_load_symptoms,
        ),
    ]