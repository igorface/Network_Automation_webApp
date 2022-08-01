from django.shortcuts import render,redirect
from dashboard.models import Devices
from .models import Vlans
from core.eapi_modules import create_eapi_conf_file
from core.credentials import get_password, get_username
from django.contrib import messages
from core.tasks import show_vlan
from pprint import pprint
import pyeapi

global username, password
username = get_username()
password = get_password()

# Create your views here.
def list_vlans(request):
    devices = Devices.objects.all()
    vlans = Vlans()
    list_of_devices = []
    set_of_vlans_on_devices = {}
    set_of_vlans_in_database = {}

    for device in Devices.objects.all():
        ip_address_from_database = device.ip_address
        print(ip_address_from_database)
        try:
            result = show_vlan.delay(f"{ip_address_from_database}", f"{username}", f"{password}")
            print(f"Result: {result}")
            raw_output = result.get()
            dict_output = raw_output['result'][0]['vlans']
            #vlan_id is a key in this dict 
            for key in dict_output:
                vlan_id = key
                vlan_name = dict_output[key]['name']
                vlan_status = dict_output[key]['status']
                obj = Vlans.objects.get_or_create(
                    number = int(vlan_id),
                    name = vlan_name,
                    status = vlan_status,
                )
                set_of_vlans_on_devices.add(key)
            print(set_of_vlans_on_devices)
            set_of_vlans_in_database.add(device.number)
        except:
            continue
    
    vlans = Vlans.objects.all()
    context = {
        'vlans': vlans,
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
        # selected_device = request.POST['device_dropdown'] 
        selected_device_list = request.POST.getlist('device_dropdown')
        if not vlan_number in range(1,4096):
            messages.error(request, 'Vlan number not in range')
            print('Vlan number not in range')
            return redirect('create_vlan')
        else:
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

            return redirect('result_of_creating_vlan')

    return render(request, 'vlans/create_vlan.html', context)

def result_of_creating_vlan(request):
    # print(type(results_of_tasks))
    # print(results_of_tasks)
    context = {
        'results': results_of_tasks,
    }
    return render(request, 'vlans/result_of_creating_vlan.html', context)

def unable_to_connect(request):
    return render(request, 'vlans/unable_to_connect.html')

def delete_vlan(request):
    devices = Devices.objects.all()
    context = {
        'devices': devices,
    }
    if request.method == 'POST':
        vlan_number_input = request.POST['vlan_number']
        vlan_number = int(vlan_number_input)
        # selected_device = request.POST['device_dropdown'] 
        selected_device_list = request.POST.getlist('device_dropdown')
        if not vlan_number in range(1,4096):
            messages.error(request, 'Vlan number not in range')
            print('Vlan number not in range')
            return redirect('delete_vlan')
        else:
            global results_of_deleting_vlan
            results_of_deleting_vlan = []
            for item in selected_device_list:
                create_eapi_conf_file(item, username, password)
                pyeapi.load_config('core/eapi.conf')
                try:
                    node = pyeapi.connect_to(f'{item}')
                    delete_vlan = node.api('vlans')
                    delete_vlan_result = delete_vlan.delete(vlan_number)
                    # delete_vlan_name_result = delete_vlan.set_name(vlan_number, vlan_name)
                    results_of_deleting_vlan.append(f'Vlan {vlan_number} was deleted on Device with IP: {item}')
                    print(f'Vlan deleted: {vlan_number}' )
                    #delete vlan from model
                    Vlans.objects.filter(number = vlan_number).detele()
                except:
                    return redirect('unable_to_connect')
            
            return redirect('result_of_deleting_vlan')

    return render(request, 'vlans/delete_vlan.html', context)

def result_of_deleting_vlan(request):
    context = {
        'results': results_of_deleting_vlan,
    }
    return render(request, 'vlans/result_of_deleting_vlan.html', context)

    