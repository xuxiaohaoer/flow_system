
from django.db import models
from flow_cut.models import Pcaps_cut
class tls_feature(models.Model):
    client_hello = models.CharField(max_length=3000)
    server_hello = models.CharField(max_length=3000)
    certificate = models.CharField(max_length=5000)
    name = models.CharField(max_length =100, default="null")
    label = models.CharField(max_length=10, default='white')

    def __str__(self):
        return self.name

# Create your models here.
