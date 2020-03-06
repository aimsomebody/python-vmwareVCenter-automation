'''
			Vcenter: ip login password
			         vm_name
'''


from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim
import atexit
from CONF import *

def wait_for_task( task):
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            print('Task has been successfully executed!.')
            return 0
        if task.info.state == 'error':
            task_done = True
            print(str(task.info.error.msg))
            return -1

def main():
   try:
      si = SmartConnectNoSSL( host = ho, user = us, pwd = password)
      atexit.register(Disconnect, si)
      content = si.content
      objView = content.viewManager.CreateContainerView( content.rootFolder, [vim.VirtualMachine], True)
      vmList = objView.view
   except Exception as e:
      print("Caught Exception : " + str(e))
   des_Vm=None
   try:
   	  for vm in vmList:
   	  	  if( vm.summary.config.name == vm_name):
   	  	  	 des_Vm = vm
   	  	  	 print(vm)
   	  	  	 break
   except Exception as e:
   	  print(str(e))
   if des_Vm is None:
   	  print(-1)
   	  return
   print("The current powerState is: {0}".format(des_Vm.runtime.powerState))
   if format(des_Vm.runtime.powerState) == "poweredOn":
       TASK = des_Vm.PowerOffVM_Task()
       wait_for_task(TASK)
       print("{0}".format(TASK.info.state))
   
   print("Destroying VM from vSphere.")
   TASK = des_Vm.Destroy_Task()
   wait_for_task(TASK)
   print("Done.")

if __name__ == "__main__":
   main()