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
    print('Creating net and opening wireshark')
    net = VNet()
    net.wireshark()

    print('Creating VM')
    vm = VM([
        Disk('example.qcow2'),
        Interface(net),
        SerialPort(ident='serial'),
    ])

    print('Opening interaction console')
    vm.console()

    print('Opening serial port')
    vm['serial'].console()

    # print('Opening other serial port')
    # sp.call(['picocom', vm['alt'].pty])


def netboot():
    print('Creating net and VM')

    # Netboot example setup:
    #   mkdir /tmp/netboot_example && cd /tmp/netboot_example
    #   wget http://deb.debian.org/debian/dists/stable/main/installer-amd64/current/images/netboot/gtk/netboot.tar.gz
    #   tar -xf netboot.tar.gz
    net = VNet(netboot_root='/tmp/netboot_example')
    vm = VM([
        System(ram_mib=1024),  # Need lots of RAM for netboot image cache
        Interface(net, netboot=True),
    ])

    print('Opening interaction console')
    vm.console()

    input('Press enter to kill VM')


def netboot_physical():
    print('Creating net')

    # Netboot example setup:
    #   mkdir /tmp/netboot_example && cd /tmp/netboot_example
    #   wget http://deb.debian.org/debian/dists/stable/main/installer-amd64/current/images/netboot/gtk/netboot.tar.gz
    #   tar -xf netboot.tar.gz
    net = VNet(internet=True, netboot_root='/tmp/netboot_example')
    net.attach_interface('enx3c18a057096c')

    input('Press enter to kill VNet')


if __name__ == '__main__':
    # multiple_machines()
    single_machine()
    # netboot()
    # netboot_physical()
