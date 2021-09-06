from django.urls import path
from .import views
urlpatterns = [
    path('/tls', views.feature_extract_tls, name='feature'),
]
