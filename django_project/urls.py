from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.profile, name='profile'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('activate/', user_views.activate, name='activate'),
    path('set-password/<otp_id>', user_views.set_password, name='set_password'),
    path('', include('advising_portal.urls'))
]
