import atexit
from pyVim.connect import SmartConnectNoSSL,Disconnect
from pyVmomi import vim

from CONF import *

def parse_si(si):
    content = si.RetrieveContent()
    object_view = content.viewManager.CreateContainerView(content.rootFolder,[], True)
    d = {}
    for obj in object_view.view:
        if isinstance(obj, vim.HostSystem):
        	d[obj] = '''-------------------
Host: %s
PowerState: %s
ConnectionState: %s'''	%(obj.summary.config.name,obj.summary.runtime.powerState,obj.summary.runtime.connectionState)
        if isinstance(obj, vim.VirtualMachine):
        	# print(str(obj.summary))
            ad = d[obj.runtime.host]
            d[obj.runtime.host] = '''%s 
	VM: %s 
	PowerState: %s
   	ConnectionState: %s''' %(ad,obj.summary.config.name,obj.summary.runtime.powerState,obj.summary.runtime.connectionState)
    for x in d:
    	print(d[x])
    return 0

def main():
    try:
        si = SmartConnectNoSSL(host = ho, user = us, pwd = password)
        atexit.register(Disconnect, si)
        parse_si(si)
    except Exception as e:
        print(str(e))
        return -1
    return 0

if __name__ == "__main__":
    main()