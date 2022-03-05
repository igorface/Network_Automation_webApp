from django.shortcuts import render,redirect
from dashboard.models import Devices
from django.forms.models import model_to_dict
from core.get_vlans import create_coroutines_list, gather_vlans
from core.get_vlans_thread import get_show_vlans_all
from core.eapi_modules import create_eapi_conf_file
from core.credentials import get_password, get_username
from django.contrib import admin,messages
import pyeapi


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
        'results': results_of_show_vlan[0],
    }
    return render(request, 'vlans/list_vlans.html', context)

def create_vlan(request):
    devices = Devices.objects.all()
    context = {
        'devices': devices,
    }
    if request.method == 'POST':
        vlan_number_input = request.POST['vlan_number']
        vlan_name = request.POST['vlan_name']
        vlan_number = int(vlan_number_input)
        selected_device = request.POST['device_dropdown'] 
        selected_device_list = request.POST.getlist('device_dropdown')
        if not vlan_number in range(1,4096):
            messages.error(request, 'Vlan number not in range')
            print('Vlan number not in range')
            return redirect('create_vlan')
        else:
            username = get_username()
            password = get_password()
            global results_of_tasks
            results_of_tasks = []
            for item in selected_device_list:
                create_eapi_conf_file(item, username, password)
                pyeapi.load_config('core/eapi.conf')
                try:
                    node = pyeapi.connect_to(f'{item}')
                    create_vlan = node.api('vlans')
                    create_vlan_result = create_vlan.create(vlan_number)
                    create_vlan_name_result = create_vlan.set_name(vlan_number, vlan_name)
                    results_of_tasks.append(f'Vlan {vlan_number} name: {vlan_name} was created on Device with IP: {item}')
                    print(f'Vlan created: {vlan_number}' )
                    print(f'Vlan name created: {vlan_name}' )
                except:
                    return redirect('unable_to_connect')
                
                # node = pyeapi.connect_to(f'{item}')
                # create_vlan = node.api('vlans')
                # # is_valid = create_vlan.isvlan(vlan_number)
                # # print(f'Is valid : {is_valid}')
                # create_vlan_result = create_vlan.create(vlan_number)
                # create_vlan_name_result = create_vlan.set_name(vlan_number, vlan_name)
                # results_of_tasks.append(f'Vlan {vlan_number} name: {vlan_name} was created on Device with IP: {item}')
                # print(f'Vlan created: {vlan_number}' )
                # print(f'Vlan name created: {vlan_name}' )

            return redirect('result_of_creating_vlan')

    return render(request, 'vlans/create_vlan.html', context)

def result_of_creating_vlan(request):
    print(type(results_of_tasks))
    print(results_of_tasks)
    context = {
        'results': results_of_tasks,
    }
    return render(request, 'vlans/result_of_creating_vlan.html', context)

def unable_to_connect(request):
    return render(request, 'vlans/unable_to_connect.html')
    