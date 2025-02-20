from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('result/', views.result, name='result'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)