import time
from pprint import pprint
from tasks import add, show_vlan, create_vlan
from celery.result import AsyncResult

# result = add.delay(1, 2)
result_0 = show_vlan.delay("10.0.0.1", "admin", "arista")
result_1 = show_vlan.delay("10.0.0.2", "admin", "arista")
result_2 = show_vlan.delay("10.0.0.101", "admin", "arista")
result_3 = show_vlan.delay("10.0.0.102", "admin", "arista")
pprint(result_0.get())
pprint(result_1.get())
pprint(result_2.get())
pprint(result_3.get())

# result_4 = create_vlan.delay("10.0.0.1", "admin", "arista")
# pprint(result_4.get())