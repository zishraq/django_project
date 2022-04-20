from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.profile_view, name='profile'),
    path('profile/', user_views.profile_view, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('activate/', user_views.activate_student_profile_view, name='activate'),
    path('set-password/<otp_id>', user_views.set_password_view, name='set_password'),
    path('forgot-password/', user_views.forgot_password_view, name='forgot_password'),
    path('reset-password/<otp_id>', user_views.reset_password_view, name='reset_password'),
    path('', include('advising_portal.urls'))
]
