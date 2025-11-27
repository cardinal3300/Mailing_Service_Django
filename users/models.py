from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Кастомный менеджер пользователей."""
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


class UserService(AbstractUser):
    """Кастомная модель пользователя."""
    username = None  # Убираем стандартное поле username
    email = models.EmailField(_("email address"), unique=True)

    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Аватар")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Номер телефона")
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name="Страна")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [
            ("view_service_users", "Просмотр списка пользователей"),
            ("block_users", "Блокировка пользователей"),
        ]

    def __str__(self):
        return self.email
