from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label="Ваше имя пользователя")
    password1 = forms.CharField(
        label="Ваш пароль",
        widget=forms.PasswordInput,
        validators=[validate_password]
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        validators=[validate_password]
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # переопределение сообщений об ошибках
        self.fields['password1'].error_messages = {
            'required': 'Это поле обязательно.',
            'password_mismatch': 'Пароли не совпадают.',
            # добавьте здесь другие сообщения об ошибках
        }


