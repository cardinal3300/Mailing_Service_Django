from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View

from mailing.forms import MailingForm, MessageForm, RecipientForm
from mailing.models import Mailing, Message, Recipient
from users.models import MailingAttempt


# Декоратор login_required для защиты CBV
@method_decorator(login_required, name="dispatch")
class HomeView(ListView):
    model = Mailing
    template_name = "mailing/home.html"
    context_object_name = "mailings"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_mailings"] = Mailing.objects.count()
        context["active_mailings"] = Mailing.objects.filter(status=Mailing.STATUS_RUNNING).count()
        context["unique_recipients"] = Recipient.objects.count()
        return context


# Получатели:
@method_decorator(login_required, name="dispatch")
class RecipientListView(ListView):
    model = Recipient
    template_name = "mailing/recipient_list.html"


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


@method_decorator(login_required, name="dispatch")
class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "mailing/recipient_confirm_delete.html"
    success_url = reverse_lazy("mailing:recipient_list")


# Сообщения:
@method_decorator(login_required, name="dispatch")
class MessageListView(ListView):
    model = Message
    template_name = "mailing/message_list.html"


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


@method_decorator(login_required, name="dispatch")
class MessageDeleteView(DeleteView):
    model = Message
    template_name = "mailing/message_confirm_delete.html"
    success_url = reverse_lazy("mailing:message_list")


# Рассылки:
@method_decorator(login_required, name="dispatch")
class MailingListView(ListView):
    model = Mailing
    template_name = "mailing/mailing_list.html"


@method_decorator(login_required, name="dispatch")
class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = "mailing/mailing_form.html"
    success_url = reverse_lazy("mailing:mailing_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Создание рассылки"
        return context


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
            # Рассылка писем
            for recipient in mailing.recipients.all():
                try:
                    send_mail(
                        mailing.message.subject,
                        mailing.message.body,
                        settings.EMAIL_HOST_USER,
                        [recipient.email],
                        fail_silently=False,
                    )
                    MailingAttempt.objects.create(mailing=mailing, recipient=recipient, status="Sent")
                except Exception as e:
                    MailingAttempt.objects.create(
                        mailing=mailing, recipient=recipient, status=f"Error: {e}", server_response=str(e)
                    )
                    messages.error(request, f"Ошибка при отправке {recipient.email}: {e}")

            messages.success(request, "Сообщения успешно отправлены.")
        except Mailing.DoesNotExist:
            messages.error(request, "Рассылка не найдена.")
        except Exception as e:
            messages.error(request, f"Произошла ошибка: {e}")

        mailings = Mailing.objects.all()
        return render(request, self.template_name, {"mailings": mailings})
