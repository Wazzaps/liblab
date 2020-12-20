"""Network and Serial interfaces"""
from liblab.vm import Device, VNet
import xml.etree.ElementTree as ET

class SerialPort(Device):
    """Serial (UART) port."""
    def __init__(self, ident=None):
        super().__init__(ident=ident)
        self.idx_in_machine = None
        self.path = None
        self._hypervisor = None
        self._machine_name = None

    @property
    def pty(self):
        """
        The path to the PTY associated with this serial port.

        Example:
            Send some data to the port:

                vm = VM([..., SerialPort()])
                port = open(SerialPort.of(vm).pty, 'wb+', buffering=0)
                port.write(b'ls -l /\\r\\n')

                print(port.read(500).decode())
        """
        dom = self._hypervisor.lookupByName(self._machine_name)
        tree = ET.fromstring(dom.XMLDesc())
        return tree.find(f"./devices/serial/target[@port='{self.idx_in_machine}']/../source").attrib['path']

    def create(self, hypervisor, machine_name, components):
        self.idx_in_machine = SerialPort.all_of(components).index(self)
        self._hypervisor = hypervisor
        self._machine_name = machine_name

    def _to_xml(self):
        return f'''
        <serial type='pty'>
            <target type='isa-serial' port='{self.idx_in_machine}'>
                <model name='isa-serial'/>
            </target>
        </serial>
        '''


class E1000Interface(Device):
    """
    A network interface (network adapter) that connects a VM to a network.

    "Interface" is an alias for "E1000Interface".

    Args:
        net: The network to connect to.
        netboot: Should netboot take boot priority over the disks.

    Example:
        Typical connection:

            Interface(VNet())

        With netboot:

            Interface(VNet(netboot_root='/tmp/my_netboot'), netboot=True)
    """
    def __init__(self, net, ident=None, netboot=False):
        assert type(net) is VNet, '`net` must be a VNet'
        super().__init__(ident=ident)
        self.net = net
        self._netboot = netboot

    def _to_xml(self):
        return f'''
        <interface type="network">
            <source network="{self.net.name}"/>
            <model type="e1000"/>
            {'<boot order="1"/>' if self._netboot else ''}
        </interface>
        '''


Interface = E1000Interface
