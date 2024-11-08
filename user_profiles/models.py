from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from fitflexproduct.models import WorkoutProgram  

class UserProfile(models.Model):
    """
    A user profile model for maintaining
    order history, purchased programs, wishlist, and personal info.

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_first_name = models.CharField(max_length=50, blank=True)
    default_last_name = models.CharField(max_length=50, blank=True)
    purchased_programs = models.ManyToManyField(WorkoutProgram, related_name='purchased_by', blank=True)
    wishlist = models.ManyToManyField(WorkoutProgram, related_name='wishlisted_by', blank=True)

    def __str__(self):
        return self.user.username
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"



@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()