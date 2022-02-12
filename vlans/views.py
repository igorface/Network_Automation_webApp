from django.shortcuts import render

# Create your views here.
def list_vlans(request):
    return render(request, 'vlans/list_vlans.html')

def create_vlan(request):
    return render(request, 'vlans/create_vlan.html')