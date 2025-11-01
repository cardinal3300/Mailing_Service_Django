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

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class UserService(AbstractUser):
    """Кастомная модель пользователя."""

    username = None  # Убираем стандартное поле username
    email = models.EmailField(_("email address"), unique=True)  # Email - уникальный идентификатор

    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Аватар")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Номер телефона")
    country = models.CharField(max_length=100, blank=True, null=True, verbose_name="Страна")

    USERNAME_FIELD = "email"  # Указываем email в качестве логина
    REQUIRED_FIELDS = []  # Убираем username из обязательных полей (оставляем только email)

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class MailingAttempt(models.Model):
    """Попытка рассылки."""

    mailing = models.ForeignKey(
        "mailing.Mailing", on_delete=models.CASCADE, verbose_name="Рассылка"
    )  # ForeignKey на модель Mailing из приложения mailing
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    status = models.CharField(max_length=50, verbose_name="Статус", blank=True, null=True)
    server_response = models.TextField(verbose_name="Ответ почтового сервера", blank=True, null=True)
    recipient = models.ForeignKey("mailing.Recipient", on_delete=models.CASCADE, verbose_name="Получатель")

    def __str__(self):
        return f"Попытка рассылки {self.mailing.message.subject} - {self.status}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
