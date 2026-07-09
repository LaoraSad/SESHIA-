from django.db import models


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True, db_column='id_categoria')
    nombre = models.CharField(max_length=80)
    tipo = models.CharField(max_length=20)
    icono = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=7, null=True, blank=True)
    color_claro = models.CharField(max_length=7, null=True, blank=True)
    es_default = models.BooleanField(default=True)
    persona = models.ForeignKey('users.Persona', on_delete=models.CASCADE, null=True, blank=True, db_column='persona_id')

    class Meta:
        db_table = 'categoria'
        indexes = [models.Index(fields=['persona', 'tipo'])]


class Transaccion(models.Model):
    id_transaccion = models.AutoField(primary_key=True, db_column='id_transaccion')
    persona = models.ForeignKey('users.Persona', on_delete=models.CASCADE, db_column='persona_id')
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, db_column='categoria_id')
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    tipo = models.CharField(max_length=20)
    fecha = models.DateField()
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transaccion'
        indexes = [
            models.Index(fields=['persona', '-fecha']),
            models.Index(fields=['persona', 'fecha', 'tipo']),
        ]
