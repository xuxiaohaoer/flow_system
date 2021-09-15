
from django.db import models
class tls_feature(models.Model):
    client_hello = models.CharField(max_length=3000)
    server_hello = models.CharField(max_length=3000)
    certificate = models.CharField(max_length=5000)
    name = models.CharField(max_length =100, default="null")
    label = models.CharField(max_length=10, default='white')

    def __str__(self):
        return self.name


class flow_feature(models.Model):
    name = models.CharField(max_length =100, default="null")
    label = models.CharField(max_length=10, default='white')
    feature = models.CharField(max_length=10000)
    def __str__(self):
        return self.name


class image_feature(models.Model):
    name = models.CharField(max_length =100, default="null")
    label = models.CharField(max_length=10, default='white')
    feature = models.CharField(max_length=10000)
    def __str__(self):
        return self.name
