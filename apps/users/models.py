from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class PersonaManager(BaseUserManager):
    def create_user(self, correo, nombre, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo es obligatorio')
        correo = self.normalize_email(correo)
        persona = self.model(correo=correo, nombre=nombre, **extra_fields)
        persona.set_password(password)
        persona.save(using=self._db)
        return persona

    def create_superuser(self, correo, nombre, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(correo, nombre, password, **extra_fields)


class Persona(AbstractBaseUser, PermissionsMixin):
    id_persona = models.AutoField(primary_key=True, db_column='id_persona')
    nombre = models.CharField(max_length=150)
    correo = models.EmailField(unique=True)
    ciclo_duracion_default = models.IntegerField(default=28)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = PersonaManager()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre']

    class Meta:
        db_table = 'persona'

    def __str__(self):
        return self.nombre