from django.db import models


class AppSettings(models.Model):
    current_date = models.DateField(
        verbose_name="Fecha actual",
    )

    class Meta:
        verbose_name = "Configuración"
        verbose_name_plural = "Configuración"

    def __str__(self):
        return f"Fecha actual: {self.current_date}"
