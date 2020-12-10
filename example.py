from liblab import VM, System, VNet, Disk, Interface, SerialPort
import subprocess as sp

def multiple_machines():
    print('Creating net and VMs')
    net = VNet()
    vms = [VM([Disk('example.qcow2'), Interface(net)]) for _ in range(4)]
    for vm in vms:
        vm.console()

    input('Press enter to kill machines (Changes will be erased!)')


def single_machine():
    print('Creating net and VM')
    vm = VM([
        Disk('example.qcow2'),
        Interface(VNet()),
        SerialPort(),
        SerialPort(ident='alt')
    ])

    print('Opening interaction console')
    vm.console()

    print('Opening serial port')
    sp.call(['picocom', SerialPort.of(vm).pty])

    # print('Opening other serial port')
    # sp.call(['picocom', SerialPort.by_id(vm, 'alt').pty])


if __name__ == '__main__':
    # single_machine()
    multiple_machines()
