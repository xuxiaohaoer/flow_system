from django.db import models

# Create your models here.
class Pcap(models.Model):
    name = models.CharField(max_length=100, default="")
    date = models.DateTimeField('data published')