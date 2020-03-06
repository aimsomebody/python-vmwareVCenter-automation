'''
			Vcenter: ip login password
			         vm_name
'''



from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim
import atexit
from CONF import *

def main():
   try:
      si = SmartConnectNoSSL( host = ho, user = us, pwd = password)
      atexit.register(Disconnect, si)
      content = si.content
      objView = content.viewManager.CreateContainerView( content.rootFolder, [vim.VirtualMachine], True)
      vmList = objView.view
      for vm in vmList:
         if(vm.summary.config.name == vm_name):
            print(vm.summary.runtime.powerState)
            print(vm.summary.runtime.connectionState)
            if(vm.summary.runtime.powerState == 'poweredOn' and  vm.summary.runtime.connectionState == 'connected'):
               vm.ShutdownGuest()
               print(1)
            else:
               print(0)
   except Exception as e:
      print("Caught Exception : " + str(e))

if __name__ == "__main__":
   main()