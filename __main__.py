from vm import VM, System, Disk, VNet, Interface
import time

# def idea():
#     client_disk = Disk('example_client.qcow2')
#     router_disk = Disk('example_router.qcow2')
#
#     a_to_router = VNet(dhcp=None)
#     b_to_router = VNet(dhcp=None)
#     client_a = VM([client_disk, Interface(a_to_router)])
#     client_b = VM([client_disk, Interface(b_to_router)])
#     router = VM([router_disk, Interface(a_to_router), Interface(b_to_router), SSHController('root@{ip}:root')])
#
#     print(Controller.of(router).cmd('ip addr show'))


if __name__ == '__main__':
    net = VNet()

    for i in range(2):
        print(f'creating vm #{i+1}')
        vm = VM([ Disk('example.qcow2'), Interface(net) ])
        vm.create()
        vm.console()

    input('Press enter to kill VMs. (All changes will be lost!)')
