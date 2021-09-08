from django.urls import path
from .import views
urlpatterns = [
    path('tls', views.feature_extract_tls, name='feature_tls'),
    path('flow', views.feature_extract_flow, name='feature_flow'),
    path('image', views.feature_extract_image, name='feature_image'),
]
