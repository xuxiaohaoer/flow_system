from django.db import models
class Questions(models.Model):
  question_text = models.CharField(max_length=200)
  pub_date = models.DateTimeField('date published')
  def __str__(self):
      return self.question_text

class Choice(models.Model):
  question = models.ForeignKey(Questions, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)
  voice = models.IntegerField(default=0)
  def __str__(self):
      return self.choice_text
# Create your models here.
