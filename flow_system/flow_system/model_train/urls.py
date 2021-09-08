from django.urls import path
from .import views
urlpatterns = [ 
    path('tls', views.train_tls, name='train_tls'),
    path('flow', views.train_HAE, name="train_HAE"),
    path('image', views.train_MT, name="train_MT"),
]
