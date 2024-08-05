from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    resume = models.FileField(null=True,max_length=500)

class UserRole(models.Model):
    ROLE_CHOICES = [
        ('jobseeker', 'JobSeeker'),
        ('recruiter', 'Recruiter'),
    ]
    user = models.OneToOneField(User, related_name='userrole', on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    user = instance

    if created:
        profile = UserProfile(user=user)
        profile.save()