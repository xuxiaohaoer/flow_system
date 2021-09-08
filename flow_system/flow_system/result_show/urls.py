from django.urls import path
from .import views
urlpatterns = [ 
    path('/tls', views.show_tls, name='show_tls'),
    path('/flow', views.show_HAE, name='show_HAE'),
    path('/image', views.show_MT, name='show_MT'),
]
