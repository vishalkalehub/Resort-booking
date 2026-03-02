from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index_view, name='index'),
    path('rooms/', rooms_view, name='rooms'),
    path('room/<int:id>/', room_detail_view, name='room_detail'),  # ✅ ADD THIS
    path('create_booking/', create_view, name='create_booking'),
    path('display_booking/', display_view, name='display_booking'),
    path('update/<int:id>/', update_booking, name='update_booking'),
    path('delete/<int:id>/', delete_booking, name='delete_booking'),
    path('gallery/', gallery_view, name='gallery'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('thank-you/', thank_you, name='thank_you'),
    path('check-availability/<int:room_id>/', check_availability, name='check_availability'),
     path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path("login/", CustomLoginView.as_view(), name="login"),
]