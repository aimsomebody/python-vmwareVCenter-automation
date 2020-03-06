'''
			Vcenter: ip login password
'''


import atexit
from pyVim import connect
from pyVmomi import vim

from CONF import *

def sizeof_fmt(num):
    for item in ['MB','GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, item)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')


def print_vm_info(virt_mach):
    summary = virt_mach.summary
    print("VM name:         ", summary.config.name)
    print("OS full name:    ", summary.config.guestFullName)
    print("Memory:          ", sizeof_fmt(summary.config.memorySizeMB))
    print("Conn State:      ", summary.runtime.connectionState)
    print("State:           ", summary.runtime.powerState)
    print("IP:              ", summary.guest.ipAddress)
    print("Boot Time:       ", summary.runtime.bootTime)
    # print(summary)
    return 0

def main():
    try:
        si = connect.SmartConnectNoSSL( host = ho, user = us, pwd = password)
        atexit.register(connect.Disconnect, si)
        content = si.RetrieveContent()
        container = content.rootFolder
        viewType = [vim.VirtualMachine]
        recursive = True
        containerView = content.viewManager.CreateContainerView( container, viewType, recursive)
        children = containerView.view
        for child in children:
            print_vm_info(child)
    except Exception as e:
        print(-1)
        return -1
    return 0

if __name__ == "__main__":
    main()
