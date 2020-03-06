'''
		Vcenter: ip login password
		         template_name  - name of VM to clone
		         new_vm_name    - name of New VM
		         resource_pool  - ip address of the Host to clone to
		         datastore_name - datastore of the Host if not provided 
		         New VM will be cloned to the first datastore of the Host
'''

from pyVmomi import vim
from pyVim.connect import SmartConnectNoSSL, Disconnect
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
            exit()

def get_obj( content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView( content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break
    return obj

def clone_vm( content, template, vm_name, si, datastore_name, resource_pool):
    datacenter = get_obj( content, [vim.Datacenter], None)
    destfolder = datacenter.vmFolder
    if datastore_name:
        datastore = get_obj( content, [vim.Datastore], datastore_name)
    else:
        objview = content.viewManager.CreateContainerView( content.rootFolder, [vim.HostSystem], True)
        esxi_hosts = objview.view
        for esxi_host in esxi_hosts:
            if esxi_host.name == resource_pool:
                storage_system = esxi_host.configManager.storageSystem
                host_file_sys_vol_mount_info = storage_system.fileSystemVolumeInfo.mountInfo
                datastore = host_file_sys_vol_mount_info[0].volume.name
                datastore = get_obj( content, [vim.Datastore], datastore)               
                break
    cluster = get_obj(content, [vim.ClusterComputeResource], None)
    host_dest = resource_pool;
    if resource_pool:
        resource_pool = get_obj(content, [vim.ResourcePool], resource_pool)
    else:
        resource_pool = cluster.resourcePool
    vmconf = vim.vm.ConfigSpec()
    destination_host = get_obj(content, [vim.HostSystem], host_dest)
    relospec = vim.VirtualMachineRelocateSpec()
    relospec.pool = destination_host.parent.resourcePool
    relospec.datastore = datastore
    clonespec = vim.vm.CloneSpec()
    clonespec.location = relospec
    print("cloning VM...")
    task = template.Clone( folder = destfolder, name = vm_name, spec = clonespec)
    wait_for_task(task)

def main():
    try:
        si = SmartConnectNoSSL( host = ho, user = us, pwd = password)
        atexit.register( Disconnect, si)
    except Exception as e:
        print(str(e))
        return -1
    content = si.RetrieveContent()
    template = None
    template = get_obj( content, [vim.VirtualMachine], template_name)
    if template:
        clone_vm( content, template, new_vm_name, si, datastore_name, resource_pool)
    else:
        print("     Template not found")

if __name__ == "__main__":
    main()