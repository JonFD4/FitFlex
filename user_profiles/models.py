from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    A user profile model

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_first_name = models.CharField(max_length=50, blank=True)
    default_last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=254, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    @property
    def full_name(self):
        return f"{self.default_first_name} {self.default_last_name}"



@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()