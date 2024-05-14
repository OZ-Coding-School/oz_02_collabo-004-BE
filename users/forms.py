from django import forms
from .models import User

class UserMBTIUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['mbti']