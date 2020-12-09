from vm import VM, System, Disk, VNet, Interface, SerialPort
import time
import subprocess as sp

if __name__ == '__main__':
    net = VNet()
    vm = VM([ Disk('example.qcow2'), Interface(net), SerialPort() ])
    vm.create()
    vm.console()

    sp.call(['picocom', SerialPort.of(vm).pty])
