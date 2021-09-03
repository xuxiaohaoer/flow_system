
from django.db import models

class tls_feature(models.Model):
    client_hello = models.CharField(max_length=3000)
    server_hello = models.CharField(max_length=3000)
    certificate = models.CharField(max_length=3000)
    name = models.CharField(max_length=1000, default='0')
    label = models.CharField(max_length=10, default='white')

    def __str__(self):
        return self.name

# Create your models here.
