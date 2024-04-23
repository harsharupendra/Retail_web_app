from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {
            'username': '',  
            'email': '',  
            'password1': '',  
            'password2': '',  
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].validators = [validate_password]
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    def clean_password2(self):
        password2 = super().clean_password2()
        password1 = self.cleaned_data.get("password1")
        if password2 and password1 and password2 != password1:
            self.add_error('password2', "The two password fields didn't match.")
        return password2