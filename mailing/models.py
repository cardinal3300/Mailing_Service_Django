from django.db import models

from users.models import UserService


class Recipient(models.Model):
    """Получатель рассылки."""
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=100, verbose_name="Имя", blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name="Фамилия", blank=True, null=True)
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"


class Message(models.Model):
    """Сообщение для рассылки."""
    subject = models.CharField(max_length=150, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")

    def __str__(self):
        return f"{self.subject}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Mailing(models.Model):
    """Рассылка."""
    STATUS_CREATED = "created"  # Создана
    STATUS_RUNNING = "running"  # Запущена
    STATUS_COMPLETED = "completed"  # Завершена
    STATUS_CHOICES = [
        (STATUS_CREATED, "Создана"),
        (STATUS_RUNNING, "Запущена"),
        (STATUS_COMPLETED, "Завершена"),
    ]

    send_time = models.DateTimeField(verbose_name="Дата и время первой отправки", blank=True, null=True)
    end_time = models.DateTimeField(verbose_name="Дата и время окончания отправки", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CREATED, verbose_name="Статус")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение")
    recipients = models.ManyToManyField(Recipient, verbose_name="Получатели")
    owner = models.ForeignKey(
        UserService, on_delete=models.CASCADE, verbose_name="Владелец", null=True, blank=True
    )  # Добавление владельца

    def __str__(self):
        return f"Рассылка: {self.message.subject} - Статус: {self.status}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
