from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView

from articles.views import articles_list, article_details, user_login, register

urlpatterns = [
    path('articles/', articles_list, name='articles_list'),
    path('articles/<slug:slug>/', article_details, name='article_details'),
    # path('login/', user_login, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('register/', register, name='register'),
    path('password-change/', PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
]