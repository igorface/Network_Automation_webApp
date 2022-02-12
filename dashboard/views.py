from django.shortcuts import render
from django.http import HttpResponse
from .models import Devices

# Create your views here.
def index(request):
    devices = Devices.objects.all()
    context = {
        'devices': devices
    }
    return render(request, 'dashboard/index.html', context)

def vlans_list(request):
    return render(request, 'dashboard/vlans_list.html')