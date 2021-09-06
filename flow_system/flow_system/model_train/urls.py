from django.urls import path
from .import views
urlpatterns = [ 
    path('', views.train_tls, name='train'),
]
