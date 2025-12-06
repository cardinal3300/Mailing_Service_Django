from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import UserService


class UserRegisterForm(UserCreationForm):
    """Форма регистрации нового пользователя по email."""
    class Meta:
        model = UserService
        fields = ["email", "password1", "password2", "avatar", "phone", "country"]

    password1 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Подтверждение пароля", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    email = forms.CharField(
        label="email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    phone = forms.CharField(
        label="Номер телефона", widget=forms.NumberInput(attrs={"class": "form-control"})
    )
    country = forms.CharField(
        label="Страна", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """Логин по email."""
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Введите email:"}), label="email")
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Введите пароль:"}))


class UserProfileForm(forms.ModelForm):
    """Редактирование профиля."""
    class Meta:
        model = UserService
        fields = ["email", "avatar", "phone", "country"]
        widgets = {
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.NumberInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"})
        }
