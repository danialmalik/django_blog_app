from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from .models import Profile, User


# This code is triggered whenever a new user has been created and saved to the database.

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Whenever User is created, create a Profile instance too for that user

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
