# BASIC  
ho = '192.168.0.117'
us = 'administrator@vsphere.local'
password = 'elma1997!Ea'

#VM state off on suspend resume  Host State
vm_name='FreeBSD-008'
# find_vm_ip='192.168.0.121'
find_host_ip = '192.168.0.118'

#clone vm
new_vm_name = 'FreeBSD-003'
datastore_name = None
resource_pool='192.168.0.112'
template_name = 'FreeBSD-001'
datastore_name='Datastore-1'
            # content, template, new_vm_name, si,
            # datastore_name, resource_pool)