from django.db import models

# Create your models here.
class Pcap(models.Model):
    nth = models.IntegerField(default=0)
    date = models.DateTimeField('data published')