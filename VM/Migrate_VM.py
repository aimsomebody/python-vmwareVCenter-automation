'''
			Vcenter: ip login password
			         vm_name        - name of The VM 
			         resource_pool  - IP of the HOST different from current host of the VM
			         datastore_name - datastore of the HOST if not provided VM will be migrated to the first datastore of the HOST
'''


import atexit
from pyVim.connect import Disconnect, SmartConnectNoSSL
from pyVmomi import vim

from CONF import *

def get_object( content, vimtype, name, disp=False):
    obj = None
    container = content.viewManager.CreateContainerView( content.rootFolder, vimtype, True)
    for c in container.view:
        if disp:
            print("c.name:" + str(c.name))
        if c.name == name:
            obj = c
            break
    return obj

def collect_template_disks( vm):
    template_disks = []
    for device in vm.config.hardware.device:
        if type(device).__name__ == "vim.vm.device.VirtualDisk":
            datastore = device.backing.datastore
            if hasattr(device.backing, 'fileName'):
                disk_desc = str(device.backing.fileName)
                drive = disk_desc.split("]")[0].replace("[", "")
                template_disks.append(device)
    return template_disks

def construct_locator( template_disks, datastore_dest_id):
    ds_disk = []
    for index, wdisk in enumerate(template_disks):
        disk_desc = str(wdisk.backing.fileName)
        drive = disk_desc.split("]")[0].replace("[", "")
        locator = vim.vm.RelocateSpec.DiskLocator()
        locator.diskBackingInfo = wdisk.backing
        locator.diskId = int(wdisk.key)
        locator.datastore = datastore_dest_id
        ds_disk.append(locator)
    return ds_disk

def wait_for_task(task):
    task_done = False
    print('Relocating.....')
    while not task_done:
        if task.info.state == 'success':
            print('Task has been successfully executed!.')
            return 0
        if task.info.state == 'error':
            task_done = True
            print(str(task.info.error.msg))
            return -1

def relocate_vm( vm_name, content, host_dest, datastore_dest = None):
    relocation_status = False
    try:
        vm = get_object(content, [vim.VirtualMachine], vm_name)
        current_host = vm.runtime.host.name
        spec = vim.VirtualMachineRelocateSpec()
        if host_dest is not None:
            if current_host == host_dest:
                raise Exception("WARNING:: destination_host can not equal "
                                "current_host")
            destination_host = get_object(content, [vim.HostSystem], host_dest)
            spec.host = destination_host
            target_esx_host = destination_host.parent.resourcePool
            spec.pool = target_esx_host
        if datastore_dest is not None:
            template_disks = collect_template_disks(vm)
            datastore_dest_id = get_object( content, [vim.Datastore], datastore_dest)
            spec.datastore = datastore_dest_id
            spec.disk = construct_locator( template_disks, datastore_dest_id)
        else:
            objview = content.viewManager.CreateContainerView( content.rootFolder, [vim.HostSystem], True)
            esxi_hosts = objview.view
            objview.Destroy()
            for esxi_host in esxi_hosts:
                if esxi_host.name == host_dest:
                    storage_system = esxi_host.configManager.storageSystem
                    host_file_sys_vol_mount_info = storage_system.fileSystemVolumeInfo.mountInfo
                    datastore = host_file_sys_vol_mount_info[0].volume.name
                    datastore = get_object(content, [vim.Datastore], datastore) 
                    template_disks = collect_template_disks(vm)              
                    spec.datastore = datastore
                    spec.disk = construct_locator(template_disks, datastore)
                    break
        task = vm.RelocateVM_Task(spec)
        wait_for_task(task)
    except Exception as e:
        print("Relocation failed for vm:",vm_name," with error:",str(e),".\nHost or VM doesn't exist or Vm is already in the mentioned host.")
        return -1

def main():
    try:
        si = SmartConnectNoSSL( host = ho, user = us, pwd = password)
        atexit.register(Disconnect, si)
        content = si.RetrieveContent()
        datastore_dest = datastore_name
        host_dest = resource_pool
        relocate_vm( vm_name, content, host_dest, datastore_dest)
    except Exception as e:
        print(str(e),'\n')
        return -1
    return 0

if __name__ == "__main__":
    main()