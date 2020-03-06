'''
			Vcenter: ip login password
			         vm_name  find_vm_ip
'''

import atexit
from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim

from CONF import *

def main():
    si = SmartConnectNoSSL( host = ho, user = us, pwd = password)
    atexit.register( Disconnect, si)
    content = si.RetrieveContent()
    vms = content.viewManager.CreateContainerView( content.rootFolder, [vim.VirtualMachine], True).view
    vm = None
    if vm_name:
        for x in vms:
            if(x.summary.config.name == vm_name):
                vm = x
    elif find_vm_ip:
        for x in vms:
            if(x.summary.guest.ipAddress == find_vm_ip):
                vm = x
    else:
        print('Argument is not given')
        return 0
    print('''Name: %s
      Path to VM: %s
      VM state: %s
      Ip: %s
      Guest OS name: %s
      Host name: %s'''%( vm.summary.config.name, vm.summary.config.vmPathName, vm.summary.runtime.powerState, summary.guest.ipAddress, vm.summary.config.guestFullName, vm.runtime.host.name))
    return 0

if __name__ == '__main__':
	main()