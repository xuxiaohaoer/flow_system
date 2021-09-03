from django.db import models

# Create your models here.

class Pcaps_cut(models.Model):
    name = models.CharField(max_length=20)
    pub_date = models.DateField('date published')
    nth = models.IntegerField()
    label = models.CharField(max_length=10, default=0)
    def __str__(self):
        return self.name