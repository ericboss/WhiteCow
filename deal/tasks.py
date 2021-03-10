from celery import shared_task
from .models import Deals
from django.core.mail import send_mail
from django.conf import settings





days = ['mon,tue,wed,thu,fri,sat,sun', 'sat,sun']
times = [5,6,7,8,20,21,22]
def send_email_scheduler():
    deals = Deals.objects.all()
    for deal in deals:
        if deal.ReceveEmail:
            if deal.days in days:
                if deal.time in times:
                    print("send email")
            else:
                pass
        else:
            pass

@shared_task
def email():
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['ericnguifo@gmail.com',]
    send_mail( subject, message, email_from, recipient_list )
    