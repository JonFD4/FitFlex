from django.contrib import admin
from .models import FAQ, UserQuestion


class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_answered', 'created_at', 'updated_at')
    search_fields = ('question', 'answer')
    list_filter = ('is_answered',)
    ordering = ('-created_at',)


class UserQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'submitted_at', 'is_reviewed')
    search_fields = ('question',)
    list_filter = ('is_reviewed',)
    ordering = ('-submitted_at',)


admin.site.register(FAQ, FAQAdmin)
admin.site.register(UserQuestion, UserQuestionAdmin)
