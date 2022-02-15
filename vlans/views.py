from django.shortcuts import render
from dashboard.models import Devices
from django.forms.models import model_to_dict
from core.get_vlans import create_coroutines_list, gather_vlans
from core.get_vlans_thread import get_show_vlans_all


# Create your views here.
def list_vlans(request):
    """ Tuple to handle ThreadExecutor"""
    hostnames = ()
    devices = Devices.objects.all()
    for device in Devices.objects.all():
        ip_address_from_database = device.ip_address
        hostnames = hostnames + (ip_address_from_database,)
        print(ip_address_from_database)
    
    results_of_show_vlan = get_show_vlans_all(hostnames)
    print(results_of_show_vlan[0])
    context = {
        "results": results_of_show_vlan[0],
    }
    print(hostnames)
    return render(request, 'vlans/list_vlans.html', context)

def create_vlan(request):
    return render(request, 'vlans/create_vlan.html')
