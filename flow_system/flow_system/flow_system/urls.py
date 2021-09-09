"""flow_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('flow_collect/', include('flow_collect.urls')),
    path('flow_cut/', include('flow_cut.urls')),
    path('feature_extract/', include('feature_extract.urls')),

    path('model_test/', include('model_test.urls')),
    path('model_train/', include('model_train.urls')),
    path('result_show/', include('result_show.urls')),
]
