from vm import VM, System, SATADisk, VNet, E1000Interface
import time

# def idea():
#     client_disk = SATADisk('example_client.qcow2')
#     router_disk = SATADisk('example_router.qcow2')
#
#     a_to_router = VNet(dhcp=None)
#     b_to_router = VNet(dhcp=None)
#     client_a = VM([client_disk, E1000Interface(a_to_router)])
#     client_b = VM([client_disk, E1000Interface(b_to_router)])
#     router = VM([router_disk, E1000Interface(a_to_router), E1000Interface(b_to_router), SSHController('root@{ip}:root')])
#
#     print(Controller.of(router).cmd('ip addr show'))


if __name__ == '__main__':
    net = VNet()
    net.create()

    for i in range(2):
        print(f'creating vm #{i+1}')
        vm = VM([SATADisk('example.qcow2'), E1000Interface(net)])
        vm.create()
        vm.console()

    input('Press enter to kill VMs. (All changes will be lost!)')
