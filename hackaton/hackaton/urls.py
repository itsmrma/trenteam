from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('result/', views.result, name='result'),
]