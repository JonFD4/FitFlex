
from django.db import models
from django.contrib.auth.models import User 
from django_summernote.fields import SummernoteTextField


class WorkoutCategory(models.Model):
    """
    Represents the workout category, i.e., whether it's a gym or home workout.
    """
    class Meta:
        verbose_name_plural = 'Workout Categories'
        
    name = models.CharField(max_length=254)  
    friendly_name = models.CharField(max_length=254)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


        
class DifficultyLevel(models.Model):
    """
    Represents the level of difficulty for a workout program.
    """
    name = models.CharField(max_length=50)  # Beginner, Intermediate, Advanced

    def __str__(self):
        return self.name

class WorkoutProgram(models.Model):
    """
    Represents an overall workout program for customers to purchase.
    """
    name = models.CharField(max_length=200) 
    description = SummernoteTextField(blank=True, null=True) 
    category = models.ForeignKey(WorkoutCategory, on_delete=models.CASCADE)  # Gym or Home
    difficulty_level = models.ForeignKey(DifficultyLevel, on_delete=models.CASCADE) 
    duration_weeks = models.IntegerField()  
    price = models.DecimalField(max_digits=6, decimal_places=2) 
    image = models.ImageField(blank=True, null=True)  
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




class Review(models.Model):
    """
    Represents a review for a workout program.
    """
    workout_program = models.ForeignKey(WorkoutProgram, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()  # using integers for ratings 1-5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.workout_program.name} by {self.user.username}'