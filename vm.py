import libvirt
import sys
import uuid
import time
import random
import os.path

hypervisor_connections = {}


class Component:
    @classmethod
    def of(cls, obj):
        for comp in cls.all_of(obj):
            return comp

    @classmethod
    def all_of(cls, obj):
        assert isinstance(
            obj, (VM, list)), 'Component.of(obj): obj must be a `VM` or a `list`'

        if isinstance(obj, VM):
            obj = obj.components

        result = []
        for comp in obj:
            if isinstance(comp, cls):
                result.append(comp)
        return result


class System(Component):
    def __init__(self, arch='x86_64', chipset='pc-q35-4.2', ram_mib=256, cpu_count=1):
        self.arch = arch
        self.chipset = chipset
        self.ram_mib = ram_mib
        self.cpu_count = cpu_count

    def to_xml(self, devices):
        # TODO: UEFI
        #     <os>
        #         <loader readonly='yes' type='pflash'>/usr/share/OVMF/OVMF_CODE.fd</loader>
        #         <nvram>/var/lib/libvirt/qemu/nvram/ninox_VARS.fd</nvram>
        #     </os>

        return '''
            <memory unit='MiB'>{ram_mib}</memory>
            <currentMemory unit='MiB'>{ram_mib}</currentMemory>
            <vcpu placement='static'>{cpu_count}</vcpu>
            <os>
                <type arch='{arch}' machine='{chipset}'>hvm</type>
                {firmware_tags}
            </os>
            <features>
                <acpi/>
                <apic/>
                <vmport state='off'/>
            </features>
            <cpu mode='host-model' check='partial'/>
            <devices>
                <emulator>/usr/bin/qemu-system-{arch}</emulator>
                <serial type='pty'>
                    <target type='isa-serial' port='0'>
                        <model name='isa-serial'/>
                    </target>
                </serial>
                <console type='pty'>
                    <target type='serial' port='0'/>
                </console>
                {devices}
                <video>
                    <model type="vga"/>
                </video>
                <graphics type="vnc" port="-1"></graphics>
                <controller type='sata' index='0'>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x1f' function='0x2'/>
                </controller>
                <controller type='pci' index='0' model='pcie-root'/>
                <controller type='pci' index='1' model='pcie-root-port'>
                    <model name='pcie-root-port'/>
                    <target chassis='1' port='0x10'/>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0' multifunction='on'/>
                </controller>
                <controller type='pci' index='2' model='pcie-root-port'>
                    <model name='pcie-root-port'/>
                    <target chassis='2' port='0x11'/>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x1'/>
                </controller>
                <controller type='pci' index='3' model='pcie-root-port'>
                    <model name='pcie-root-port'/>
                    <target chassis='3' port='0x12'/>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x2'/>
                </controller>
                <controller type='pci' index='4' model='pcie-root-port'>
                    <model name='pcie-root-port'/>
                    <target chassis='4' port='0x13'/>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x3'/>
                </controller>
                <controller type='pci' index='5' model='pcie-root-port'>
                    <model name='pcie-root-port'/>
                    <target chassis='5' port='0x14'/>
                    <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x4'/>
                </controller>
                <input type='mouse' bus='ps2'/>
                <input type='keyboard' bus='ps2'/>
            </devices>
        '''.format(
            ram_mib=self.ram_mib,
            cpu_count=self.cpu_count,
            arch=self.arch,
            chipset=self.chipset,
            firmware_tags='',
            devices=devices
        )


class Disk(Component):
    def __init__(self, image_path, linked_clone=False):
        assert image_path.endswith('.qcow2'), 'Images must be QCow2'
        self.image_path = os.path.abspath(image_path)
        self.linked_clone = linked_clone

        if self.linked_clone:
            pass  # TODO
        else:
            self.clone_path = self.image_path


class SATADisk(Disk):
    def to_xml(self):
        return f'''
        <disk type='file' device='disk'>
            <driver name='qemu' type='qcow2'/>
            <source file='{self.clone_path}'/>
            <target dev='sda' bus='sata'/>
        </disk>
        '''


class VM:
    _CREATE_TRIES = 10

    @staticmethod
    def present_components(components):
        return str(components)

    def __str__(self):
        return VM.present_components(self.components)

    def __init__(self, components=None, hypervisor_uri='qemu:///system'):
        if components is None:
            components = []
        if System.of(components) is None:
            components.append(System())

        self.components = components
        self.hypervisor_uri = hypervisor_uri
        self._conn = None
        self._dom = None

    def create(self):
        if self.hypervisor_uri not in hypervisor_connections:
            hypervisor_connections[self.hypervisor_uri] = libvirt.open(
                self.hypervisor_uri)

        self._conn = hypervisor_connections[self.hypervisor_uri]

        # Gather devices xml
        devices_xml = ''
        for device_type in [SATADisk]:
            for device in device_type.all_of(self):
                device.to_xml()
                devices_xml += device.to_xml()

        for i in range(VM._CREATE_TRIES):
            try:
                self._uuid = str(uuid.uuid4())
                self.name = f'llm_{hex(random.randint(0, 0xffffffff))[2:]}'

                xml = '''
                <domain type='kvm'>
                    <name>{name}</name>
                    <uuid>{uuid}</uuid>
                    {system}
                </domain>
                '''.format(
                    name=self.name,
                    uuid=self._uuid,
                    system=System.of(self).to_xml(devices_xml)
                )
                self._dom = self._conn.createXML(xml)
                break
            except libvirt.libvirtError:
                if i == VM._CREATE_TRIES-1:
                    raise
                time.sleep(3)

    def destroy(self):

        self._dom.destroy()
