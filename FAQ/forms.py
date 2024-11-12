from django import forms
from .models import UserQuestion, FAQ


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']
        widgets = {
            'answer': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }
        labels = {
            'question': 'Question',
            'answer': 'Answer',
        }


class UserQuestionForm(forms.ModelForm):
    class Meta:
        model = UserQuestion
        fields = ['question']
        widgets = {
            'question': forms.Textarea(
                attrs={
                    'placeholder': 'Ask your question here...',
                    'rows': 3
                }
            ),
        }
        labels = {
            'question': '',
        }
