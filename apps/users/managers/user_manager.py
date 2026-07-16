from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Manager personalizado para el modelo User.

    Se encarga de crear usuarios y superusuarios utilizando
    el correo electrónico como identificador principal.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Crea y guarda un usuario con el correo electrónico y la contraseña proporcionados.

        Args:
            email (str): Correo electrónico del usuario.
            password (str, optional): Contraseña del usuario.
            **extra_fields: Campos adicionales del modelo User.

        Returns:
            User: Instancia del usuario creada.

        Raises:
            ValueError: Si el correo electrónico no es proporcionado.
        """
        if not email:
            raise ValueError("El correo electrónico es obligatorio.")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crea y guarda un superusuario con permisos administrativos.

        Args:
            email (str): Correo electrónico del administrador.
            password (str, optional): Contraseña del administrador.
            **extra_fields: Campos adicionales del modelo User.

        Returns:
            User: Instancia del superusuario creada.

        Raises:
            ValueError: Si los permisos administrativos no son correctos.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self.create_user(
            email=email,
            password=password,
            **extra_fields,
        )

