"""
Virtual machine abstraction
"""
import libvirt
import sys
import uuid
import time
import atexit
import string
import random
import os.path
import subprocess as sp

_hypervisor_connections = {}


class Component:
    """Part of a `VM` that typically defines a `Device` or `System` information.

    Example:
        After creating a VM with a component like so:

            my_component = SATADisk('...')
            machine = VM([my_component])

        You may retrieve it by calling `Component.of` or `Component.all_of`:

            assert SATADisk.of(machine) is my_component
            assert SATADisk.all_of(machine)[0] is my_component
    """
    @classmethod
    def of(cls, obj):
        """Get the first matching component from a VM or list of components.

        Example:
            The `System` component is a common "singleton" component, which is a good use case for `Component.of`:

                machine = VM()
                System.of(machine).arch  # => "x86_64"
        """
        for comp in cls.all_of(obj):
            return comp

    @classmethod
    def all_of(cls, obj):
        """Get a list of all matching components from a VM or list of components.

        Example:
            Get all disks of a machine:

                machine = VM([SATADisk('a.qcow2'), SATADisk('a.qcow2')])
                print(Disk.all_of(machine))  # => [<SATADisk object at 0x7f055e9823a0>, <SATADisk object at 0x7f055e982400>]

                for disk in Disk.all_of(machine):
                    print(disk.image_path)  # => '/img/a.qcow2', '/img/b.qcow2'
        """
        assert isinstance(obj, (VM, list)), \
            'Component.of(obj): obj must be a `VM` or a `list`'

        if isinstance(obj, VM):
            obj = obj.components

        result = []
        for comp in obj:
            if isinstance(comp, cls):
                result.append(comp)
        return result


class System(Component):
    """Describes the CPU, Chipset, RAM, and Platform Devices of the VM.

    Args:
        arch: The architecture of the VM (default: x86_64)
        chipset: The chipset of the VM (default: pc-q35-4.2)
        ram_mib: RAM in MiB allocated to the VM (default: 256MiB)
        cpu_count: The number of cores allocated to the VM (default: 1)
    """
    def __init__(self, arch='x86_64', chipset='pc-q35-4.2', ram_mib=256, cpu_count=1):
        self.arch = arch
        self.chipset = chipset
        self.ram_mib = ram_mib
        self.cpu_count = cpu_count

    def _to_xml(self, devices):
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


class Device(Component):
    """A `Component` that needs to be initialized and destroyed, and adds a device to the libvirt XML."""
    def create(self, machine_name, components):
        pass

    def destroy(self):
        pass

    def _to_xml(self):
        raise NotImplementedError


class Disk(Device):
    """A Storage device backed by a QCow2 image, and linked-cloned by default.

    Use one of the subclasses (such as `SATADisk`).

    Example:
        Create a linked clone disk:

            SATADisk('example.qcow2')

        Create a live disk (All changes made in VM are saved):

            SATADisk('example.qcow2', linked_clone=False)
    """
    _LINKED_CLONES_DIR = '/tmp/liblab_disks'
    def __init__(self, image_path, linked_clone=True):
        assert image_path.endswith('.qcow2'), 'Images must be QCow2'
        self.image_path = os.path.abspath(image_path)
        self._linked_clone = linked_clone
        self.idx_in_machine = None
        self.live_image_path = None

    @staticmethod
    def _create_linked_clone(image_path, clone_name):
        assert os.path.exists(image_path), f'Disk image not found: {image_path}'
        clone_path = os.path.join(Disk._LINKED_CLONES_DIR, clone_name)
        assert not os.path.exists(clone_path), f'Linked clone name conflict: {clone_path} (when creating clone of: {image_path})'
        if not os.path.exists(Disk._LINKED_CLONES_DIR):
            os.mkdir(Disk._LINKED_CLONES_DIR)

        sp.check_output([
            'qemu-img', 'create',
            '-f', 'qcow2',
            '-b', image_path,
            clone_path
        ])

        return clone_path

    def __str__(self):
        if self._linked_clone:
            return f'{type(self).__name__}(base={repr(self.image_path)}, clone={repr(self.live_image_path)})'
        else:
            return f'{type(self).__name__}({repr(self.image_path)})'

    def create(self, machine_name, components):
        self.idx_in_machine = Disk.all_of(components).index(self)
        if self._linked_clone:
            self.live_image_path = Disk._create_linked_clone(self.image_path, clone_name=f'{machine_name}-disk{self.idx_in_machine}.qcow2')
        else:
            self.live_image_path = self.image_path

    def destroy(self):
        if self._linked_clone:
            try:
                os.unlink(self.live_image_path)
            except FileNotFoundError:
                pass


class SATADisk(Disk):
    """`Disk` with a SATA interface.
    """
    def _to_xml(self):
        assert self.live_image_path, 'Please call `Disk.create` first'
        return f'''
        <disk type='file' device='disk'>
            <driver name='qemu' type='qcow2'/>
            <source file='{self.live_image_path}'/>
            <target dev='sd{string.ascii_lowercase[self.idx_in_machine]}' bus='sata'/>
        </disk>
        '''


Disk = SATADisk


class E1000Interface(Device):
    def __init__(self, source):
        assert type(source) is VNet, '`source` must be a VNet'
        self.source = source

    def create(self, machine_name, components):
        self.source.create(weak=True)

    def _to_xml(self):
        return f'''
        <interface type="network">
            <source network="{self.source.name}"/>
            <model type="e1000"/>
        </interface>
        '''


Interface = E1000Interface


class VM:
    """Define a virtual machine from a list of `Component`s.

    The machine will be given a random UUID and name (in the format 'llm_xxxxxxxx').

    Args:
        components: A list of `Component`s that define the VM. A `System` is added automatically if absent
        persistent: Does the machine (and it's temporary resources) survive if Python dies?
        hypervisor_uri: The hypervisor to create the VM in (`qemu:///system` by default)

    Example:
        Creating the machine:

            # Doesn't have a disk, will be created but won't boot
            machine = VM()
            # Enough to boot, has default System() parameters
            machine = VM([SATADisk('example.qcow2')])
            # Machine with extra resources
            machine = VM([
                System(ram_mib=512, cpu_count=2),
                SATADisk('example.qcow2'),
            ])
            # Machine with alternative architecture (Not implemented)
            machine = VM([
                System(arch='arm'),
                SATADisk('example.qcow2'),
            ])
            # With context manager
            components = [SATADisk('example.qcow2')]
            with VM(components) as machine:
                machine.console()
    """
    _CREATE_TRIES = 10

    @staticmethod
    def pretty_format_components(components):
        """Return a pretty representation of the given components.

        TODO: Currently not pretty
        """
        return str(components)

    def __str__(self):
        return VM.pretty_format_components(self.components)

    def __init__(self, components=None, persistent=False, hypervisor_uri='qemu:///system'):
        if components is None:
            components = []
        if System.of(components) is None:
            components.append(System())

        self.components = components
        self._hypervisor_uri = hypervisor_uri
        self._persistent = persistent
        self._libvirt = None
        self._dom = None
        self._was_destroyed = False
        self.name = None
        self._uuid = None

    def create(self):
        """Create the machine, and initialize all devices."""
        if self._hypervisor_uri not in _hypervisor_connections:
            _hypervisor_connections[self._hypervisor_uri] = libvirt.open(
                self._hypervisor_uri)

        self._libvirt = _hypervisor_connections[self._hypervisor_uri]

        # Attempt to recreate VM multiple times - in case of uuid/name conflict or OOM
        for i in range(VM._CREATE_TRIES):
            try:
                self._uuid = str(uuid.uuid4())
                self.name = f'llm_{hex(random.randint(0, 0xffffffff))[2:]}'

                # Gather devices xml
                devices_xml = ''
                for device in Device.all_of(self):
                    device.create(self.name, self.components)
                    devices_xml += device._to_xml()

                xml = '''
                <domain type='kvm'>
                    <name>{name}</name>
                    <uuid>{uuid}</uuid>
                    {system}
                </domain>
                '''.format(
                    name=self.name,
                    uuid=self._uuid,
                    system=System.of(self)._to_xml(devices_xml)
                )

                # Create the domain
                self._dom = self._libvirt.createXML(xml)
                break
            except libvirt.libvirtError:
                # We failed to create the VM, destroy all devices
                for device in Device.all_of(self):
                    try:
                        device.destroy()
                    except libvirt.libvirtError:
                        pass

                # Retry if it's not the last iteration
                if i == VM._CREATE_TRIES-1:
                    raise
                time.sleep(3)

        if not self._persistent:
            atexit.register(self.destroy)

    def destroy(self):
        """Destroy the machine and all devices."""
        if self._was_destroyed:
            return

        try:
            self._dom.destroy()
        except libvirt.libvirtError:
            pass

        for device in Device.all_of(self):
            try:
                device.destroy()
            except libvirt.libvirtError:
                pass

        self._was_destroyed = True

    def console(self):
        """Spawn a virt-manager console of the machine."""
        sp.call(['virt-manager', '--connect', self._hypervisor_uri, '--show-domain-console', self._uuid])

    def __enter__(self):
        self.create()
        return self

    def __exit__(self, _exc_type, _exc_value, _traceback):
        self.destroy()


class VNet:
    """Define a virtual network, connecting guests, the host, and (optionally) the internet together.

    Args:
        internet: Should the VM have access to the host's network (i.e. the internet)?
        persistent: Should the network survive if Python dies?
        hypervisor_uri: The hypervisor to create the network in (`qemu:///system` by default)

    Example:
        Two machines in a network:

            net = VNet()
            net.create()
            components = [SATADisk('example.qcow2'), E1000Interface(net)]
            vm1 = VM(components)
            vm2 = VM(components)
            vm1.create()
            vm2.create()
    """
    _CREATE_TRIES = 10

    def __init__(self, internet=False, persistent=False, hypervisor_uri='qemu:///system'):
        self._internet = internet
        self._persistent = persistent
        self._hypervisor_uri = hypervisor_uri
        self._libvirt = None
        self._net = None
        self._uuid = None
        self.name = None

        # -1 = strong reference, a single destroy will destroy the machine
        # 0+ = weak references, reaching 0 will destroy the machine
        self._weak_counter = 0

    def create(self, weak=False):
        """Create the network."""
        if self._hypervisor_uri not in _hypervisor_connections:
            _hypervisor_connections[self._hypervisor_uri] = libvirt.open(
                self._hypervisor_uri)

        self._libvirt = _hypervisor_connections[self._hypervisor_uri]

        if self._weak_counter != -1 and weak:
            self._weak_counter += 1
        elif not weak:
            self._weak_counter = -1

        # Attempt to recreate VNet multiple times - in case of uuid/name conflict or OOM
        for i in range(VNet._CREATE_TRIES):
            try:
                self._uuid = str(uuid.uuid4())
                self.name = f'lln_{hex(random.randint(0, 0xffffffff))[2:]}'

                # TODO: Subnet allocation
                xml = f'''
                <network>
                    <name>{self.name}</name>
                    <uuid>{self._uuid}</uuid>
                    <bridge name="{self.name}" stp="off" delay="0"/>
                    {'<forward mode="nat"/>' if self._internet else ''}
                    <ip address="10.0.0.1" netmask="255.255.255.0">
                        <dhcp>
                            <range start="10.0.0.2" end="10.0.0.254"/>
                        </dhcp>
                    </ip>
                </network>
                '''

                # Create the network
                self._net = self._libvirt.networkCreateXML(xml)
                break
            except libvirt.libvirtError:
                # Retry if it's not the last iteration
                if i == VNet._CREATE_TRIES-1:
                    raise
                time.sleep(3)

        if not self._persistent:
            atexit.register(self.destroy)

    def destroy(self):
        """Destroy the network."""
        if self._weak_counter == -1 or self._weak_counter == 1:
            try:
                self._net.destroy()
            except libvirt.libvirtError:
                pass

        self._weak_counter -= 1

    def __enter__(self):
        self.create()
        return self

    def __exit__(self, _exc_type, _exc_value, _traceback):
        self.destroy()

    def __del__(self):
        self.destroy()
