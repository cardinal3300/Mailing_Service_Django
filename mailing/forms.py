from django import forms
from .models import Mailing, Message, Recipient
from django.core.exceptions import ValidationError


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ["first_name", "last_name", "email", "comment"]

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите имя"
        })
        self.fields["last_name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите фамилию"
        })
        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите email"
        })
        self.fields["comment"].widget.attrs.update({
            "class": "form-control",
            "type": "text"
        })

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        if Recipient.objects.filter(email="email").exists():
            raise ValidationError("Получатель с таким email уже существует.")
        return cleaned_data



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["subject", "body"]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields["subject"].widget.attrs.update({
            "class": "form-control"
        })
        self.fields["body"].widget.attrs.update({
            "class": "form-control",
            "type": "text"
        })

    def clean(self):
        cleaned_data = super().clean()
        subject = cleaned_data.get("subject")

        if Message.objects.filter(subject="subject").exists():
            raise ValidationError("Сообщение с такой темой уже существует.")
        return cleaned_data


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ["send_time", "end_time", "status", "message", "owner", "recipients"]
        widgets = {
            "send_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "recipients": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)

        self.fields["send_time"].widget.attrs.update({
            "class": "form-control"
        })

        self.fields["end_time"].widget.attrs.update({
            "class": "form-control"
        })
        self.fields["status"].widget.attrs.update({
            "class": "form-control"
        })

        self.fields["message"].widget.attrs.update({
            "class": "form-control"
        })

        self.fields["owner"].widget.attrs.update({
            "class": "form-control"
        })
