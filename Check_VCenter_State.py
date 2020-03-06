from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim
import atexit

from CONF import *

def main():
    try:
        si = SmartConnectNoSSL( host = ho, user = us, pwd = password)
        atexit.register(Disconnect, si)
        print(1)
        return 0
    except:
        print(0)
        return -1
    return 0

if __name__ == "__main__":
    main()