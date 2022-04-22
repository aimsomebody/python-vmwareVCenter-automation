# BASIC  
ho = '192.168.0.117'
us = 'administrator@vsphere.local'
password = 'password'

#VM state off on suspend resume  Host State
vm_name='FreeBSD-008'
# find_vm_ip='192.168.0.121'
find_host_ip = '192.168.0.116'

#clone vm
new_vm_name = 'FreeBSD-009'
datastore_name = None
resource_pool='192.168.0.118'
template_name = 'FreeBSD-001'
cluster='Res'
# datastore_name='Datastore-3'
            # content, template, new_vm_name, si,
            # datastore_name, resource_pool)
