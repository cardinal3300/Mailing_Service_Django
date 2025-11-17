import os

from django.core.mail import send_mail
from django.utils import timezone
from dotenv import load_dotenv

from .models import MailingAttempt

load_dotenv()

def send_mailing(mailing):
    """Отправка рассылки по требованию."""
    recipients = mailing.recipients.all()

    for recipient in recipients:
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=[recipient.email],
                recipient_list=[recipient.email],
            )
            status = "SUCCESS"
            server_response = "OK"
        except Exception as e:
            status = "FAILED"
            server_response = str(e)

        MailingAttempt.objects.create(
            mailing=mailing,
            status=status,
            server_response=server_response,
            recipient=recipient,
        )

    mailing.status = mailing.STATUS_COMPLETED
    mailing.end_time = timezone.now()
    mailing.save()
