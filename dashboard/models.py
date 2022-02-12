from django.db import models

# Create your models here.
class Devices(models.Model):
    hostname = models.CharField(max_length=200)
    ip_address = models.GenericIPAddressField()
    vendor = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    software_version = models.CharField(max_length=100)
    is_used = models.BooleanField(default=False)

def __str__(self):
    return self.hostname