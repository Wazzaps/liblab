"""Serial and QEMU debug ports"""
from liblab.vm import Device
import xml.etree.ElementTree as ET

class SerialPort(Device):
    """ISA Serial port"""
    def __init__(self, ident=None):
        super().__init__(ident=ident)
        self.idx_in_machine = None
        self.path = None
        self._hypervisor = None
        self._machine_name = None

    @property
    def pty(self):
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
