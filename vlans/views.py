from django.shortcuts import render,redirect
from dashboard.models import Devices
from django.forms.models import model_to_dict
from core.get_vlans import create_coroutines_list, gather_vlans
from core.get_vlans_thread import get_show_vlans_all
from django.contrib import admin,messages


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
    return render(request, 'vlans/list_vlans.html', context)

def create_vlan(request):
    devices = Devices.objects.all()
    context = {
        'devices': devices,
    }
    if request.method == 'POST':
        print("HELLO !!!")
        vlan_number_input = request.POST['vlan_number']
        vlan_name = request.POST['vlan_name']
        vlan_number = int(vlan_number_input)
        print(type(vlan_number))
        if not vlan_number in range(1,4096):
            messages.error(request, 'Vlan number in range')
            print('Vlan number not in range')
            return redirect('create_vlan')
        else:
            print('Vlan number in range')

    else:
        return render(request, 'vlans/create_vlan.html')
    return render(request, 'vlans/create_vlan.html', context)

