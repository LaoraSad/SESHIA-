from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.users.managers.user_manager import UserManager


class User(AbstractUser):
    """
    Representa a una usuaria registrada en la aplicación.

    Este modelo personaliza ``AbstractUser`` para utilizar el correo
    electrónico como identificador principal de autenticación.

    Además, almacena la duración promedio estimada del ciclo menstrual,
    la cual se utiliza para predecir futuros ciclos.

    Responsibilities:
        - Gestionar la autenticación de la usuaria.
        - Almacenar la información básica de la cuenta.
        - Conservar la duración promedio estimada del ciclo.
    """

    username = None
    
    objects = UserManager()

    email = models.EmailField(
        unique=True,
        verbose_name="Correo electrónico",
    
    )

    predicted_cycle_length = models.PositiveSmallIntegerField(
        default=28,
        validators=[
            MinValueValidator(20),
            MaxValueValidator(45),
        ],
        verbose_name="Duración promedio del ciclo",
        help_text=(
            "Duración promedio estimada del ciclo menstrual "
            "utilizada para realizar predicciones."
        ),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        ordering = ["first_name", "last_name"]
        verbose_name = "Usuaria"
        verbose_name_plural = "Usuarias"

    @property
    def full_name(self):
        """
        Retorna el nombre completo de la usuaria.
        """
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
    
        return self.full_name
