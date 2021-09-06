from django.urls import path
from .import views
urlpatterns = [ 
    path('', views.show_tls, name='show'),
]
