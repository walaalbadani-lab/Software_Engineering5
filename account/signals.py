from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db import transaction
from .models import Notification

@receiver(post_save, sender=User)
def send_welcome_notification_and_email(sender, instance, created, **kwargs):
    if created:
        # 1. إنشاء الإشعار في قاعدة البيانات
        Notification.objects.create(
            recipient=instance,
            message="مرحباً بك! تم إنشاء حسابك بنجاح في موقع دعوات إلكترونية.",
            link="/"
        )
        
        # 2. إرسال البريد بأمان بعد التثبيت النهائي للبيانات في قاعدة البيانات
        if instance.email:
            def send_email_action():
                try:
                    send_mail(
                        subject='مرحباً بك في موقع دعوات إلكترونية',
                        message=f'أهلاً بك يا {instance.username},\n\nشكراً لتسجيلك في موقعنا لدعوات الإلكترونية. نحن سعداء بانضمامك إلينا!',
                        from_email='admin@invitations.com',
                        recipient_list=[instance.email],
                        fail_silently=True
                    )
                except Exception as e:
                    print(f"Error sending email: {e}")

            transaction.on_commit(send_email_action)