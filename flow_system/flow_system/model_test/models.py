from django.db import models

# Create your models here.
class TlsRes(models.Model):
    name = models.CharField(max_length=1000)
    result = models.CharField(max_length=10, default='none')
    
    def __str__(self):
        return self.name

class FlowRes(models.Model):
    name = models.CharField(max_length=1000)
    result = models.CharField(max_length=10, default='none')

    def __str__(self):
        return self.name


class ImageRes(models.Model):
    name = models.CharField(max_length=1000)
    result = models.CharField(max_length=10, default='none')
    def __str__(self):
        return self.name

