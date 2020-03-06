'''
			Vcenter: ip login password
			         find_host_ip
'''



from pyVim.connect import SmartConnectNoSSL,Disconnect 
from pyVmomi import vim
import atexit

from CONF import *

def main():
    try:
        si = SmartConnectNoSSL( host = ho, user = us, pwd = password)
        atexit.register(Disconnect, si)
    except Exception as e:
        print(str(e))
        return -1
    content = si.RetrieveContent()
    host = None
    object_view = content.viewManager.CreateContainerView( content.rootFolder, [vim.HostSystem], True).view
    for obj in object_view:
        if obj.summary.config.name == find_host_ip:
            host = obj
            break
    if host is not None:
        if isinstance(host.parent,vim.ClusterComputeResource):
            tp = host.parent.name+' (Cluster)'
        else:
            tp= 'Datacenter'
        print("Location:         ", tp)
        print("Host:             ", host.summary.config.name)
        print("Host OS:          ", host.summary.config.product.fullName)
        print("Con State:        ", host.summary.runtime.connectionState)
        print("Power:            ", host.summary.runtime.powerState)
        print("Maintenance mode: ", host.summary.runtime.inMaintenanceMode)
    else:
    	print('0')
    return 0

if __name__ == "__main__":
    main()