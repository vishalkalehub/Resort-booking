from django.contrib import admin
from django.urls import path
from bookingapp.views import *

from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index_view, name='index'),          # 👈 HOME PAGE
    path('index/', index_view, name='index'),    # 👈 OPTIONAL (same view)

    path('rooms/', rooms_view, name='rooms'),
    path('create_booking/', create_view, name='create_booking'),
    path('display_booking/', display_view, name='display_booking'),
    path('update/<int:id>/', update_booking, name='update_booking'),
    path('delete/<int:id>/', delete_booking, name='delete_booking'),
    path('gallery/', gallery_view, name='gallery'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('thank-you/', thank_you, name='thank_you'),
    
]




