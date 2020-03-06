'''
      Vcenter: ip login password
               find_host_ip
'''


from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim
import atexit
import ssl
import socket
import hashlib
    
from CONF import *

def wait_for_task(task):
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            return 0
        if task.info.state == 'error':
            print(task.info.error.msg)
            exit()

def getsslThumbprint(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    wrappedSocket = ssl.wrap_socket(sock)
    ret_print = None
    try:
      wrappedSocket.connect((ip, 443))
    except:
      response = False
    else:
      der_cert_bin = wrappedSocket.getpeercert(True)
      pem_cert = ssl.DER_cert_to_PEM_cert(wrappedSocket.getpeercert(True))
      thumb_sha1 = hashlib.sha1(der_cert_bin).hexdigest()
      ret_print = ':'.join([thumb_sha1[i:i+2] for i in range(0, len(thumb_sha1), 2)])
    wrappedSocket.close()
    # print(ret_print)
    if ret_print is not None:
      return ret_print
    else:
      print(-1)
      exit()

def main():
   try:
      si = SmartConnectNoSSL( host = ho, user = us, pwd = password)
      atexit.register(Disconnect, si)
      content = si.content
      location = content.rootFolder
      folder = None
      objView = content.viewManager.CreateContainerView( location, [vim.Datacenter], True).view
      for DC in objView:
          if isinstance(DC,vim.Datacenter):
            folder = DC.hostFolder
            break
      clus_folder=None
      if 'cluster' in globals():
          clus = content.viewManager.CreateContainerView( location, [vim.ClusterComputeResource], True).view
          for x in clus:
            if(x.name==cluster):
              clus_folder = x
              break
   except Exception as e:
      print("Caught Exception : " + str(e))
      return -1
   ip = find_host_ip
   finger_print = getsslThumbprint(ip)
   hostspec = vim.host.ConnectSpec( hostName = ip, userName = 'root', password = password, sslThumbprint = finger_print,  force = True)
   if clus_folder is None:
     # print('if')
     task = folder.AddStandaloneHost( spec = hostspec, addConnected = True)
   else:
     # print('else')
     task = clus_folder.AddHost( spec = hostspec, asConnected = True)
   wait_for_task(task)
   print(1)

if __name__ == "__main__":
   main()