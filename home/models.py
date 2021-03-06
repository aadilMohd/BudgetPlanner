from django.contrib.auth.models import User
from django.db import models
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey


# Create your models here.
class Budget(models.Model):
    id = models.IntegerField(null=False,auto_created=True,primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(null=False)
    category = models.CharField(max_length=100,null=False)
    description = models.CharField(max_length=100,null=True)
    cost = models.IntegerField(null=False)

class PieChart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    figure = models.ImageField(upload_to='static/figures/')
    timestamp = models.DateTimeField(auto_now_add=True)
