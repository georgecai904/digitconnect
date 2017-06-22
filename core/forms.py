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


class NewUserForm(BasicForm):

    class Meta:
        model = User
        fields = ('username', 'password', 'email',)


class ChangeEmailForm(BasicForm):
    class Meta:
        model = User
        fields = ('email', )


class ChangePasswordForm(BasicForm):
    old_password = forms.CharField(widget=forms.PasswordInput)
    repeated_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'repeated_password', )