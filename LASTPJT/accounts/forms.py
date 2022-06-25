from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
    
        for field in self.fields:
            self.fields[field].help_text=None
            self.fields[field].label=''

        self.fields['username'].widget.attrs['placeholder'] = "아이디"
        self.fields['password1'].widget.attrs['placeholder'] = "비밀번호"
        self.fields['password2'].widget.attrs['placeholder'] = "비밀번호 확인"


    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['introduce','imgfile',]
        widgets = {
            'introduce':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'나의 취미, 영화 취향 등 자유롭게 작성해보세요',
            }),
        }


