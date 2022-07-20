from django.contrib.auth import get_user_model

from celery import shared_task 
from django.core.mail import send_mail
from django.conf import settings

@shared_task(bind = True)
def send_mail_task(email):
    
        mail_subject = "Hi! celery testing"
        message = "if you are liking my content,"
        to_email = email 
        return send_mail(
            subject = mail_subject,
            message = message,
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [to_email],
            fail_silently=True,)
        
