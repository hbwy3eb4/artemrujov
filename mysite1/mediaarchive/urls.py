from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.media_archive, name='media_archive'),
] 