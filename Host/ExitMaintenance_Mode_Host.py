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
        atexit.register( Disconnect, si)
    except Exception as e:
        print(str(e))
        return -1
    s=False
    content = si.RetrieveContent()
    object_view = content.viewManager.CreateContainerView( content.rootFolder, [vim.HostSystem], True).view
    for obj in object_view:
        if obj.summary.config.name == find_host_ip:
            host = obj
            s = True
            break
    if s:
        if host.runtime.powerState == 'poweredOn' and obj.summary.runtime.inMaintenanceMode == True:
            host.ExitMaintenanceMode( timeout = 0)
            print(1)
        else:
            print(0)
    else:
        print('Not Found!')
    # host = si.content.searchIndex.FindByDnsName(None,find_host_ip,False)
    # if host is not None:
    #     print('1')
    # else:
    # 	print('0')
    return 0

if __name__ == "__main__":
    main()