from django.db import models
from dashboard.models import Devices

# Create your models here.
class Vlans(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=32)
    status = models.CharField(max_length=15,default='passive')
def __str__(self):
    return self.number