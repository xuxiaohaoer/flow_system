from django.contrib import admin
from .models import tls_feature
from .models import flow_feature
from .models import image_feature
admin.site.register(tls_feature)
admin.site.register(flow_feature)
admin.site.register(image_feature)
# Register your models here.
