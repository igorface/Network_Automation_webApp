from django.contrib import admin
from .models import Devices

# Register your models here.
# class DevicesAdmin(admin.ModelAdmin):
    # list_display = ('hostname', 'ip_address', 'vendor', 'model', 'software_version', 'is_used')
    # list_display_links = ('id', 'hostname')
    # search_fields = ('hostname', 'ip_address', 'vendor', 'model', 'software_version')
    
admin.site.register(Devices)