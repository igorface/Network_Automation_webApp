import pyeapi
from pprint import pprint
node = pyeapi.connect(host='10.0.0.1', username= 'admin', password='arista')
output = node.execute(['show vlan'])
pprint(output)

pyeapi.load_config('eapi.conf')
node_1 = pyeapi.connect_to('veos01')
create_vlan = node_1.api('vlans')
create_vlan_123 = create_vlan.delete(123)
print(create_vlan_123)
# get the vlan api and enable autorefresh
#vlans = node.api('vlans')