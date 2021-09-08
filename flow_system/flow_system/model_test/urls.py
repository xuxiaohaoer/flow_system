from django.urls import path
from .import views
urlpatterns = [ 
    path('/tls', views.test_tls, name='test_tls'),
    path('/flow', views.test_HAE ,name='test_HAE'),
    path('/image', views.test_MT, name='test_MT'),
]
