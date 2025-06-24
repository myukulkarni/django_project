from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_otp_email(name, email, otp):
    send_mail(
        subject="Email Verification OTP",
        message=f"Hi {name},\n\nYour OTP is: {otp}\n\nThanks for registering!",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )

@shared_task
def send_welcome_email(email):
    send_mail(
        subject="Welcome to Platform 🎉",
        message="Hi there! 🎓\n\nYour account has been successfully verified. Welcome aboard!",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
