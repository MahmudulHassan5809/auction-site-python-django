from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = '1. User'


class Profile(models.Model):
    USER_CHOICES = (
        ('1', 'Bidder'),
        ('2', 'Seller'),
    )

    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name='user_profile')
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=50, blank=True, null=True)

    user_type = models.CharField(
        max_length=10, choices=USER_CHOICES)

    active = models.BooleanField(default=True)
    email_confirmed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = '2. Profile'

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    try:
        if created:
            Profile.objects.create(user=instance)
        else:
            instance.user_profile.save()
    except Exception as e:
        pass
