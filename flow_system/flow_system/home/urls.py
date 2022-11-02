from django.urls import path
from .import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [ 
    path('', views.index, name='home'),
    path('login', views.login, name='login'),
    path('recoverpw', views.pages_recoverpw, name='recoverpw'),
    path('pages-register', views.pages_register, name='register'),
    path('test', views.index_test, name='test')
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)