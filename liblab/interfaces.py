"""Network interfaces"""
from liblab.vm import Device, VNet


class E1000Interface(Device):
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
