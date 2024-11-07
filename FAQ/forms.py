from django import forms
from .models import UserQuestion

class UserQuestionForm(forms.ModelForm):
    class Meta:
        model = UserQuestion
        fields = ['question']
        widgets = {
            'question': forms.Textarea(attrs={'placeholder': 'Ask your question here...', 'rows': 3}),
        }
        labels = {
            'question': '',
        }
