from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, TemplateView, UpdateView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import redirect, get_object_or_404
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from .forms import UserRegisterForm, UserLoginForm, UserService, UserProfileForm


User = get_user_model()


@method_decorator(cache_page(60*5), name="dispatch")
class UsersListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Страница списка пользователей.
        Доступ:
            - Только менеджеры (группа "Менеджеры"),
        Контекст:
            - users: список всех пользователей системы."""

    model = User
    template_name = "users/users_list.html"
    context_object_name = "users"
    permission_required = ("users.view_service_users",)


@login_required
@permission_required("users.block_users", raise_exception=True)
def toggle_user_block(request, user_id: int):
    """Блокировка или разблокировка пользователя.
        Доступ:
            - Только менеджеры
        Логика:
            - Менеджер не может заблокировать сам себя
            - Переключает поле is_active."""

    user = get_object_or_404(User, pk=user_id)
    if user.id == request.user.id:
        # Менеджер не может заблокировать самого себя
        return redirect(reverse_lazy("users:users_list"))
    user.is_active = not user.is_active
    user.save()
    return redirect(reverse_lazy("users:users_list"))


class CustomPasswordResetView(PasswordResetView):
    """Кастомный класс PasswordResetView для сброса пароля."""
    template_name = "users/password_reset.html"
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Кастомный класс PasswordResetConfirmView для сброса пароля."""
    template_name = "users/password_reset_confirm.html"
    form_class = SetPasswordForm
    success_url = reverse_lazy("users:password_reset_complete")

    def form_valid(self, form):
        messages.success(self.request, "Пароль успешно изменен!")
        return super().form_valid(form)


class ActivateAccountView(TemplateView):
    """Активирует пользователя по ссылке из email."""
    template_name = "users/activation_result.html"

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            user = None
        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Email подтверждён! Теперь войдите в систему.")
        else:
            messages.error(request, "Ссылка активации недействительна.")
        return redirect("users:login")


class UserRegisterView(CreateView):
    """Регистрация нового пользователя с отправкой email-подтверждения."""
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False    # пользователь пока не активен
        user.save()
        # Генерация токена
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        # Формирование ссылки
        activate_url = self.request.build_absolute_uri(
            reverse_lazy("users:activate", kwargs={"uidb64": uid, "token": token})
        )
        # Письмо
        subject = "Подтверждение регистрации"
        message = render_to_string("users/activation_email.html", {
            "user": user,
            "activate_url": activate_url,
        })
        send_mail(subject, message, None, [user.email])
        messages.success(
            self.request,
            "Регистрация прошла успешно! Подтвердите email, чтобы войти."
        )
        return redirect(self.success_url)


class UserProfileView(LoginRequiredMixin, TemplateView):
    """Профиль пользователя"""
    template_name = "users/profile.html"


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля пользователя"""
    model = UserService
    form_class = UserProfileForm
    template_name = "users/edit_profile.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        """Редактируем именно профиль текущего пользователя"""
        return self.request.user


class UserLoginView(LoginView):
    """Вход пользователя."""
    template_name = "users/login.html"
    authentication_form = UserLoginForm

    def form_valid(self, form):
        messages.success(self.request, f"Вы вошли как {form.get_user().email}")
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    """Выход пользователя с редиректом на главную"""
    template_name = "users/logout.html"
    next_page = reverse_lazy("mailing:home")
