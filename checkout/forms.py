from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name','last_name', 'email']  

    def __init__(self, *args, **kwargs):
        """
        Add placeholders, classes, remove auto-generated labels,
        and set autofocus on the first field.
        """
        super().__init__(*args, **kwargs)

        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last name',
            'email': 'Email Address',
        }

       
        self.fields['first_name'].widget.attrs['autofocus'] = True




        for field in self.fields:
            placeholder = f'{placeholders[field]} *' if self.fields[field].required else placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'  
            self.fields[field].label = False  
