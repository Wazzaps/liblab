"""Network interfaces"""
from liblab.vm import Device, VNet


class E1000Interface(Device):
    def __init__(self, source, ident=None):
        assert type(source) is VNet, '`source` must be a VNet'
        super().__init__(ident=ident)
        self.source = source

    def _to_xml(self):
        return f'''
        <interface type="network">
            <source network="{self.source.name}"/>
            <model type="e1000"/>
        </interface>
        '''


Interface = E1000Interface
