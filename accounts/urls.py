from django.contrib import admin
from django.urls import path,include,re_path
from . import views
from django.contrib.auth.views import(
LoginView,LogoutView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
)

urlpatterns = [
        re_path(r'^$', views.HomeAccount.as_view(),name='account'),
        re_path(r'^login/', LoginView.as_view(template_name='accounts/login.html'),name='login'),
        path('logout/', LogoutView.as_view(template_name='home.html'),name='logout'),
        path('register/', views.Register.as_view(),name='register'),
        path('profile/', views.Profile.as_view(),name='profile'),
        path('activate/<str:username>/<str:activate>', views.ActivateAccount,name='activate_account'),
        path('activate/form', views.ActivateAccountForm.as_view(),name='activate_account_form'),
        re_path(r'^profile/edit', views.EditProfile.as_view(),name='edit_profile'),
        re_path(r'^profile/change-password$', views.ChangePassword.as_view(),name='change_password'),
        re_path(r'^profile/reset-password$', PasswordResetView.as_view(template_name='accounts/password_reset_form.html'),name='password_reset'),
        path('profile/reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
        re_path(r'^profile/reset-password/done', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),name='password_reset_done'),
        re_path(r'^profile/reset-password/complete', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),name='password_reset_complete'),

]
