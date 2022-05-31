import time
import pyeapi
from celery import Celery
from pprint import pprint
from core.eapi_modules import create_eapi_conf_file

app = Celery('tasks', backend='redis://redis:6379/0', broker='redis://redis:6379/0')

@app.task(name='tasks.add')
def add(x, y):
	total = x + y
	print('{} + {} = {}'.format(x, y, total))
	time.sleep(10)
	return total

@app.task(name='tasks.show_vlan')
def show_vlan(device_ip, username, password):
    node = pyeapi.connect(host=f'{device_ip}', username= f'{username}', password=f'{password}')
    output = node.execute(['show vlan'])
    pprint(output)
    return output

@app.task(name='tasks.create_vlan')
def create_vlan(device_ip, username, password):
    # node = pyeapi.connect(host=f'{device_ip}', username= f'{username}', password=f'{password}', transport='https', port=443)
    create_eapi_conf_file(device_ip, username, password)
    pyeapi.load_config('core/eapi.conf')
    node = pyeapi.connect_to(f'{device_ip}')
    vlans = node.api('vlans')
    vlans.autorefresh = True
    output = []
    for vlan in list(vlans.values()):
        output.append(("   Vlan Id: {vlan_id}, Name: {name}".format(**vlan)))
        print(("   Vlan Id: {vlan_id}, Name: {name}".format(**vlan)))
        # pprint(output)
    return output