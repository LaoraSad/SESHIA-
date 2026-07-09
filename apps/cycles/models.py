from django.db import models


class Fase(models.Model):
    id_fase = models.AutoField(primary_key=True, db_column='id_fase')
    nombre = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    orden = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'fase'


class NivelEnergia(models.Model):
    id_energia = models.AutoField(primary_key=True, db_column='id_energia')
    nivel = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    valor = models.IntegerField(unique=True)

    class Meta:
        db_table = 'nivel_energia'


class EstadoAnimo(models.Model):
    id_estado_animo = models.AutoField(primary_key=True, db_column='id_estado_animo')
    nombre = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    icono = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'estado_animo'


class Ciclo(models.Model):
    id_ciclo = models.AutoField(primary_key=True, db_column='id_ciclo')
    persona = models.ForeignKey('users.Persona', on_delete=models.CASCADE, db_column='persona_id')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    duracion_esperada = models.IntegerField(default=28)
    notas = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        db_table = 'ciclo'
        indexes = [models.Index(fields=['persona', '-fecha_inicio'])]


class CicloFase(models.Model):
    id_ciclo_fase = models.AutoField(primary_key=True, db_column='id_ciclo_fase')
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE, db_column='ciclo_id')
    fase = models.ForeignKey(Fase, on_delete=models.CASCADE, db_column='fase_id')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    class Meta:
        db_table = 'ciclo_fase'
        indexes = [models.Index(fields=['ciclo', 'fecha_inicio', 'fecha_fin'])]


class RegistroCiclo(models.Model):
    id_registro = models.AutoField(primary_key=True, db_column='id_registro')
    ciclo = models.ForeignKey(Ciclo, on_delete=models.CASCADE, db_column='ciclo_id')
    fecha = models.DateField()
    energia = models.ForeignKey(NivelEnergia, on_delete=models.CASCADE, db_column='energia_id')
    animo = models.ForeignKey(EstadoAnimo, on_delete=models.CASCADE, db_column='animo_id')
    sintomas = models.JSONField(default=list)
    notas = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        db_table = 'registro_ciclo'
        unique_together = ['ciclo', 'fecha']