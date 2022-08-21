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

class Vlans(models.Model):
    name = models.CharField(max_length=200)
    vlan_id = models.PositiveIntegerField()
    
    def __str__(self):
        return self.vlan_id

class Physical_Interfaces(models.Model):
    name = models.CharField(max_length=100)
    enabled = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    native_vlan = models.ForeignKey(Vlans, on_delete=models.CASCADE)
    trunk_vlans = models.ManyToManyField(Vlans, related_name='tagged_vlans')

    def __str__(self):
        return self.name


