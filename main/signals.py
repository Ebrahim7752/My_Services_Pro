# main/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ApiToken

@receiver(post_save, sender=User)
def create_api_token(sender, instance, created, **kwargs):
    """
    عند إنشاء مستخدم جديد، يقوم بإنشاء ApiToken تلقائيًا
    """
    if created:
        ApiToken.objects.create(user=instance)
