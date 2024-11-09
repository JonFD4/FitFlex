
from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)  

    def __init__(self, *args, **kwargs):
        """
        Add placeholders, remove labels, set autofocus on first field,
        and apply custom CSS classes.
        """
        super().__init__(*args, **kwargs)

       
        placeholders = {
            'default_first_name': 'First Name',
            'default_last_name': 'Last Name',
        }

        self.fields['default_first_name'].widget.attrs['autofocus'] = True

       
        for field in self.fields:
            if field in placeholders:
                placeholder = placeholders.get(field, '')
                if self.fields[field].required:
                    placeholder += ' *'
                self.fields[field].widget.attrs['placeholder'] = placeholder

          
            self.fields[field].widget.attrs['class'] = 'border-blue rounded-0 profile-form-input'

            
            self.fields[field].label = False
