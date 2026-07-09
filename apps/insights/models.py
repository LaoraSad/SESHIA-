from django.db import models


class Insight(models.Model):
    id_insight = models.AutoField(primary_key=True, db_column='id_insight')
    persona = models.ForeignKey('users.Persona', on_delete=models.CASCADE, db_column='persona_id')
    mensaje = models.TextField()
    fuente = models.CharField(max_length=10)
    generado_en = models.DateTimeField(auto_now_add=True)
    total_transacciones = models.IntegerField(default=0)

    class Meta:
        db_table = 'insight'
        indexes = [models.Index(fields=['persona', '-generado_en'])]