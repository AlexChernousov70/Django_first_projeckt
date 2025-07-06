from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _ # импортируем функцию для перевода текста
from django.contrib.auth import get_user_model


User = get_user_model()

class LoginForm(AuthenticationForm):
    """
    Кастомная форма входа
    """
    username = forms.CharField(
        label='Логин или Email',
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'form-control',
            'placeholder': 'Введите логин или email'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем классы Bootstrap ко всем полям
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })
            field.label = ''  # Убираем стандартные лейблы

    error_messages = {
        'invalid_login': _(
            "Неверное имя пользователя или пароль. "
            "Учтите, что оба поля могут быть чувствительны к регистру."
        ),
        'inactive': _("Этот аккаунт неактивен."),
    }

    username = forms.CharField(
        label='Логин или Email',
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'form-control',
            'placeholder': 'Введите логин или email'
        })
    )

    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        }),
    )

class RegisterForm(UserCreationForm):
    """
    Кастомная форма регистрации
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        }),
        label='Email'
    )

    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше имя'
        }),
        label='Имя'
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваша фамилия'
        }),
        label='Фамилия'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Кастомизация полей
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Придумайте логин'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Придумайте пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
        self.fields['password2'].error_messages = {
            'password_mismatch': 'Пароли не совпадают. Пожалуйста, введите одинаковые пароли в оба поля.', 'required': 'Это поле обязательно для заполнения'
        }

        # Убираем help_text
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None

    def clean_email(self):
        """Валидация уникальности email"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует")
        return email

    def clean_password1(self):
        """Дополнительная валидация пароля"""
        password1 = self.cleaned_data.get('password1')
        if password1.isdigit():
            raise ValidationError("Пароль не может состоять только из цифр")
        if password1.lower() == self.cleaned_data.get('username', '').lower():
            raise ValidationError("Пароль не должен совпадать с логином")
        return password1