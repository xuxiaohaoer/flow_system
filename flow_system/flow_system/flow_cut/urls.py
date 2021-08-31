from django.urls import path 
from .import views
urlpatterns = [
    path('', views.cut, name='cut'),
]
