from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
urlpatterns = [
    path('', views.home, name='home'),
    path('result/', views.result, name='result'),
    path('cronologia/', views.cronologia, name='cronologia'),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)