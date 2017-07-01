from django import forms
from django.contrib.auth.models import User


class BasicForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BasicForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class LoginInForm(BasicForm):

    class Meta:
        model = User
        fields = ('username', 'password')
        labels = {
            'username': '用户名',
            'password': '密码'
        }
        help_texts = {
            'username': None
        }
        widgets = {
            'password': forms.PasswordInput
        }


class NewUserForm(BasicForm):

    class Meta:
        model = User
        fields = ('username', 'password', 'email',)
        labels = {
            'username': '用户名',
            'password': '密码',
            'email': '电子邮箱'
        }
        help_texts = {
            'username': None
        }
        widgets = {
            'password': forms.PasswordInput
        }


class ChangeEmailForm(BasicForm):
    class Meta:
        model = User
        fields = ('email', )
        labels = {
            'email': '电子邮箱'
        }


class ChangePasswordForm(BasicForm):
    old_password = forms.CharField(widget=forms.PasswordInput, label="原密码")
    repeated_password = forms.CharField(widget=forms.PasswordInput, label="确认密码")

    class Meta:
        model = User
        fields = ('old_password', 'password', 'repeated_password', )
        labels = {
            'password': '新密码',
        }
        widgets = {
            'password': forms.PasswordInput
        }