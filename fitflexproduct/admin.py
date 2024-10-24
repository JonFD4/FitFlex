from django.contrib import admin
from .models import WorkoutProgram, WorkoutCategory, DifficultyLevel, Review
from django_summernote.admin import SummernoteModelAdmin 


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0  


class WorkoutProgramAdmin(SummernoteModelAdmin): 
    inlines = (ReviewInline,)  

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

    summernote_fields = ('description',)  
# Admin class for managing workout categories
class WorkoutCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name', 
        'name',          
    )
    ordering = ('name',) 

# Admin class for managing difficulty levels
class DifficultyLevelAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    ordering = ('name',)  

# Admin class for managing reviews separately
class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = (
        'workout_program',  
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

    search_fields = ('workout_program__name', 'user__username')  
    list_filter = ('rating',)  
    ordering = ('-created_at',)  


admin.site.register(WorkoutProgram, WorkoutProgramAdmin)
admin.site.register(WorkoutCategory, WorkoutCategoryAdmin)
admin.site.register(DifficultyLevel, DifficultyLevelAdmin)
admin.site.register(Review, ReviewAdmin)
