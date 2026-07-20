from django.db import migrations


def seed_categories(apps, schema_editor):
    Category = apps.get_model("finances", "Category")

    categories = [
        ("Salario", "income", "💼"),
        ("Freelance", "income", "💻"),
        ("Regalos", "income", "🎁"),
        ("Otros ingresos", "income", "💸"),
        ("Hogar", "expense", "🏠"),
        ("Alimentación", "expense", "🍽️"),
        ("Transporte", "expense", "🚗"),
        ("Cuidado menstrual", "expense", "🌸"),
        ("Compras", "expense", "🛍️"),
        ("Ocio", "expense", "🎉"),
    ]

    for name, category_type, icon in categories:
        Category.objects.get_or_create(
            name=name,
            category_type=category_type,
            defaults={
                "icon": icon,
                "is_default": True,
                "is_active": True,
                "user": None,
            },
        )


def reverse_seed_categories(apps, schema_editor):
    Category = apps.get_model("finances", "Category")

    Category.objects.filter(is_default=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("finances", "0003_transaction_is_active"),
    ]

    operations = [
        migrations.RunPython(
            seed_categories,
            reverse_seed_categories,
        ),
    ]
