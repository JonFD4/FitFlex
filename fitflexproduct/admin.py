from django.contrib import admin
from .models import WorkoutProgram, WorkoutCategory, DifficultyLevel, Review

# Inline class to display reviews within the WorkoutProgram admin interface
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0  

# Admin class for managing workout programs
class WorkoutProgramAdmin(admin.ModelAdmin):
    inlines = (ReviewInline,)  # Attach the reviews inline to the WorkoutProgram admin page

    list_display = (
        'name',
        'category',
        'difficulty_level',
        'price',
        'duration_weeks',
        'created_at',
        'image',  
    )

    search_fields = ('name', 'category__name', 'difficulty_level__name')  # Make category and difficulty searchable
    ordering = ('name',) 

# Admin class for managing workout categories
class WorkoutCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name', 
        'name',          
    )
# Admin class for managing difficulty levels
class DifficultyLevelAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )

# Admin class for managing reviews separately
class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = (
        'user',
        'rating',
        'comment',
        'created_at',
    )

    list_display = (
        'workout_program',  
        'user',
        'rating',
        'comment',
        'created_at',
    )

    search_fields = ('workout_program__name', 'user__username')  # Allows searching by workout program and user
    list_filter = ('rating',)  # Allows filtering by rating

# Register your models with the admin site
admin.site.register(WorkoutProgram, WorkoutProgramAdmin)
admin.site.register(WorkoutCategory, WorkoutCategoryAdmin)
admin.site.register(DifficultyLevel, DifficultyLevelAdmin)
admin.site.register(Review, ReviewAdmin)
