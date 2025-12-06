from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    UserRegisterView,
    UserProfileView,
    UserLoginView,
    UserLogoutView,
    ProfileEditView,
    ActivateAccountView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    UsersListView,
    toggle_user_block
)

app_name = "users"

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("activate/<uidb64>/<token>/", ActivateAccountView.as_view(), name="activate"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="edit_profile"),
    path("list/", UsersListView.as_view(), name="users_list"),
    path("toggle-block/<int:user_id>/", toggle_user_block, name="toggle_user_block"),

    # Восстановление пароля
    path("password_reset/", CustomPasswordResetView.as_view(template_name="users/password_reset_form.html"),
         name="password_reset"),

    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
         name="password_reset_done"),

    path("reset/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),
         name="password_reset_confirm"),

    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
         name="password_reset_complete"),
]
