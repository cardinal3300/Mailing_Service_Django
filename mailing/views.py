from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View
from mailing.forms import MailingForm, MessageForm, RecipientForm
from mailing.models import Mailing, Message, Recipient
from mailing.services import MailingAttempt


# Декоратор login_required для защиты CBV
@method_decorator([cache_page(60*5), login_required], name="dispatch")
class HomeView(ListView):
    model = Mailing
    template_name = "mailing/home.html"
    context_object_name = "mailings"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        attempts = MailingAttempt.objects.filter(mailing__owner=user)
        context["total_mailings"] = attempts.count()
        context["active_mailings"] = attempts.filter(status=Mailing.STATUS_RUNNING).count()
        context["unique_recipients"] = Recipient.objects.count()
        context["total_attempts"] = attempts.count()
        context["success_attempts"] = attempts.filter(is_success=True).count()
        context["failed_attempts"] = attempts.filter(is_success=False).count()
        return context


# Получатели:
@method_decorator([cache_page(60*5), login_required], name="dispatch")
class RecipientListView(ListView):
    model = Recipient
    template_name = "mailing/recipient_list.html"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


@method_decorator(login_required, name="dispatch")
class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mailing/recipient_form.html"
    success_url = reverse_lazy("mailing:recipient_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Добавление получателя"
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "mailing/recipient_form.html"
    success_url = reverse_lazy("mailing:recipient_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Редактирование получателя"
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "mailing/recipient_confirm_delete.html"
    success_url = reverse_lazy("mailing:recipient_list")


# Сообщения:
@method_decorator([cache_page(60*5), login_required], name="dispatch")
class MessageListView(ListView):
    model = Message
    template_name = "mailing/message_list.html"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


@method_decorator(login_required, name="dispatch")
class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Создание сообщения"
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message_form.html"
    success_url = reverse_lazy("mailing:message_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Редактирование сообщения"
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class MessageDeleteView(DeleteView):
    model = Message
    template_name = "mailing/message_confirm_delete.html"
    success_url = reverse_lazy("mailing:message_list")


# Рассылки:
@method_decorator([cache_page(60*5), login_required], name="dispatch")
class MailingListView(ListView):
    model = Mailing
    template_name = "mailing/mailing_list.html"

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Менеджеры").exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=user)


@method_decorator(login_required, name="dispatch")
class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Создание рассылки"
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Редактирование рассылки"
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = "mailing/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing:mailing_list")


# Отправка рассылок:
@method_decorator(login_required, name="dispatch")
class SendMailView(View):
    template_name = "mailing/send_mailing.html"

    def get(self, request, *args, **kwargs):
        mailings = Mailing.objects.all()
        return render(request, self.template_name, {"mailings": mailings})

    def post(self, request, *args, **kwargs):
        mailing_id = request.POST.get("mailing_id")

        try:
            mailing = Mailing.objects.get(pk=mailing_id)
        except Mailing.DoesNotExist:
            messages.error(request, "Рассылка не найдена.")
            return redirect("mailing:send_mailing")

        recipients = mailing.recipients.all()

        for recipient in recipients:

            # 1) Инициация попытки (записываем факт начала)
            attempt = MailingAttempt.objects.create(
                mailing=mailing,
                recipient=recipient,
                status="Started",
                server_response="Attempt initiated",
                is_success=False
            )

            # 2) Отправка
            try:
                send_mail(
                    mailing.message.subject,
                    mailing.message.body,
                    settings.EMAIL_HOST_USER,
                    [recipient.email],
                    fail_silently=False,
                )

                # обновление попытки
                attempt.status = "Success"
                attempt.server_response = "Email sent"
                attempt.is_success = True
                attempt.save()

            except Exception as e:
                attempt.status = "Failed"
                attempt.server_response = str(e)
                attempt.is_success = False
                attempt.save()

                messages.error(request, f"Ошибка при отправке {recipient.email}: {e}")

        messages.success(request, "Попытка рассылки выполнена.")
        return redirect("mailing:send_mailing")
