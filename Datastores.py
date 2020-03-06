import atexit
from pyVim.connect import SmartConnectNoSSL,Disconnect
from pyVmomi import vim

from CONF import *

def sizeof_fmt(num):
    for item in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, item)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')

def main():
    try:
        si = SmartConnectNoSSL( host = ho, user = us, pwd = password)
        atexit.register(Disconnect, si)
        content = si.RetrieveContent()
        objview = content.viewManager.CreateContainerView(content.rootFolder,[vim.HostSystem],True)
        esxi_hosts = objview.view
        datastores = content.viewManager.CreateContainerView(content.rootFolder,[vim.Datastore],True).view
        for esxi_host in esxi_hosts:
            state = esxi_host.summary.runtime.connectionState
            powerstate = esxi_host.summary.runtime.powerState
            print("{}\t{}\t{}".format("ESXi Host:    ", esxi_host.name,state))
            if(state == "connected" and powerstate=="poweredon"):
                storage_system = esxi_host.configManager.storageSystem
                host_file_sys_vol_mount_info = storage_system.fileSystemVolumeInfo.mountInfo
                for host_fs in host_file_sys_vol_mount_info:
                    if host_fs.volume.type == "VMFS":
                        for dt in datastores:
                            if(host_fs.volume.name == dt.summary.name):
                                print("{}\t{}".format("Datastore:     ", host_fs.volume.name))
                                print("{}\t{}".format("Capacity:      ", sizeof_fmt(host_fs.volume.capacity)))
                                print("{}\t{}".format("Free space:    ", sizeof_fmt(dt.summary.freeSpace)))
            else:
                print('poweredoff')
    except Exception as e:
        print(str(e),'\n')
        return -1
    return 0

if __name__ == "__main__":
    main()