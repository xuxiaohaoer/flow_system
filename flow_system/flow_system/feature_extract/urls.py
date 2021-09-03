from django.urls import path
from .import views
urlpatterns = [
    path('', views.feature_extract, name='feature'),
]
