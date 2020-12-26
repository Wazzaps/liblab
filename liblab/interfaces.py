"""Network and Serial interfaces"""
from liblab.vm import Device, VNet
import subprocess
import xml.etree.ElementTree as ET


class HIDProxy:
    """
    Interface with an HIDProxy (Keyboard and mouse simulation device).

    - Connect an Arduino Leonardo compatible board (I used a cheap beetle usb knockoff)
    - Flash the "hidproxy.ino" sketch on it
    - Connect a USB to UART adapter with Adapter.tx -> Arduino.rx and vice-versa
    - Connect the Arduino to the target PC and the UART adapter to yours

    Commands:
        identify: Blink the LED and send the version on the serial port
        mouse_click: Click the given mouse button
        TODO: the rest
    """
    def __init__(self, port):
        self._port = port
        # TODO: replace with pyserial for baud rate
        self._fd = open(port, 'wb', buffering=0)
        self._fd.write(b'\x00')  # Enter raw mode

    def identify(self):
        self._fd.write(b'\x01')  # Identify command

    def _tty_mode(self):
        self._fd.write(b'\x02')  # Switch to TTY mode (default)

    def mouse_click(self, button='left'):
        if button == 'left':
            self._fd.write(b'\x09\x01')
        elif button == 'right':
            self._fd.write(b'\x09\x02')
        elif button == 'middle':
            self._fd.write(b'\x09\x04')


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

    def console(self):
        subprocess.call(['picocom', self.pty])

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
