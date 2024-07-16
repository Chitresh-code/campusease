from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .import views, Hod_views, Staff_views, Student_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),

    # Login Page Path
    path('', views.LOGIN, name='login'),
    path('doLogin', views.doLogin, name='doLogin'),

    # Hod Panel Path
    path('Hod/Home', Hod_views.HOME, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
