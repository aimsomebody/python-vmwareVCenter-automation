'''
			Vcenter: ip login password
			         find_host_ip
'''



from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim
import atexit
from CONF import *

def wait_for_task(task):
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            return 0
        if task.info.state == 'error':
            task_done = True
            print(str(task.info.error.msg))
            exit()

def main():
   try:
      si = SmartConnectNoSSL( host = ho, user = us, pwd = password)
      atexit.register(Disconnect, si)
      content = si.content
      objView = content.viewManager.CreateContainerView( content.rootFolder, [vim.HostSystem], True)
      hostList = objView.view
   except Exception as e:
      print("Caught Exception : " + str(e))
   des_host = None
   ip = find_host_ip
   try:
     for host in hostList:
       if isinstance(host,vim.HostSystem) and host.summary.config.name == ip:
         des_host = host
         break
   except Exception as e:
      print(str(e))
      exit()
   if des_host is None:
   	  print(0)
   	  return
   TASK = None
   if isinstance(des_host.parent,vim.ClusterComputeResource):
      TASK = des_host.Destroy()
   else:
      TASK = des_host.parent.Destroy()
   wait_for_task(TASK)
   print(1)

if __name__ == "__main__":
   main()