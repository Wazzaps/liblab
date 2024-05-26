"""Virtual machine abstraction"""

import dataclasses
import json
import random
import struct
import subprocess as sp
import time
import uuid
from os import PathLike

import libvirt
from typing_extensions import Self

import liblab.keycodes

_hypervisor_connections = {}


class Component:
    """
    Part of a `VM` that typically defines a `Device` or `System` information.

    Example:
        After creating a VM with a component like so:

            my_component = SATADisk('...')
            machine = VM([my_component])

        You may retrieve it by calling `Component.of` or `Component.all_of`:

            assert SATADisk.of(machine) is my_component
            assert SATADisk.all_of(machine)[0] is my_component
    """

    def __init__(self, ident: str | None = None):
        self._ident = ident

    @classmethod
    def by_id(cls, obj, ident) -> Self | None:
        """
        Get the first matching component from a VM or list of components by its `ident`.

        Shortened form of this is available in VM class, see example below

        Example:
            If you have multiple SerialPorts, giving them IDs helps you refer to them:

                machine = VM([SerialPort(ident='main'), SerialPort(ident='alt')])
                SerialPort.by_id(machine, 'main').pty  # => /dev/pty/1
                SerialPort.by_id(machine, 'alt').pty  # => /dev/pty/2

                # Shortened (but not type-safe) form
                machine['main'].pty  # => /dev/pty/1
                machine['alt'].pty  # => /dev/pty/2

        """
        for comp in cls.all_of(obj):
            if comp._ident == ident:
                return comp

    @classmethod
    def of(cls, obj) -> Self | None:
        """
        Get the first matching component from a VM or list of components.

        Example:
            The `System` component is a common "singleton" component, which is a good use case for `Component.of`:

                machine = VM()
                System.of(machine).arch  # => "x86_64"
        """
        for comp in cls.all_of(obj):
            return comp

    @classmethod
    def all_of(cls, obj: "VM | list[Self]") -> list[Self]:
        """
        Get a list of all matching components from a VM or list of components.

        Example:
            Get all disks of a machine:

                machine = VM([SATADisk('a.qcow2'), SATADisk('a.qcow2')])
                print(Disk.all_of(machine))  # => [<SATADisk object at 0x7f055e9823a0>, <SATADisk object at 0x7f055e982400>]

                for disk in Disk.all_of(machine):
                    print(disk.image_path)  # => '/img/a.qcow2', '/img/b.qcow2'
        """
        assert isinstance(obj, (VM, list)), "Component.of(obj): obj must be a `VM` or a `list`"

        if isinstance(obj, VM):
            obj = obj.components

        result = []
        for comp in obj:
            if isinstance(comp, cls):
                result.append(comp)
        return result


class System(Component):
    """
    Describes the CPU, Chipset, RAM, and Platform Devices of the VM.

    Args:
        arch: The architecture of the VM (default: x86_64)
        chipset: The chipset of the VM (default: pc-q35-4.2)
        ram_mib: RAM in MiB allocated to the VM (default: 256MiB)
        cpu_count: The number of cores allocated to the VM (default: 1)
    """

    def __init__(
        self,
        arch="x86_64",
        chipset="pc-q35-6.2",
        ram_mib=256,
        cpu_count=1,
        efi_image: PathLike | None = None,
        ident=None,
    ):
        super().__init__(ident=ident)
        self.arch = arch
        self.chipset = chipset
        self.ram_mib = ram_mib
        self.cpu_count = cpu_count
        self.efi_image = efi_image

    def _to_xml(self, vm: "VM", devices_xml: str):
        # TODO: QXL/Spice graphics
        # TODO: memballoon
        # TODO: virtio-rng
        from liblab import NVRAMImage

        efi_snippet = ""
        if self.efi_image:
            efi_snippet += f'<loader readonly="yes" type="pflash">{self.efi_image}</loader>'

        if efi_nvram := NVRAMImage.of(vm):
            efi_snippet += f"<nvram>{efi_nvram.live_image_path}</nvram>"

        return """
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
            <cpu mode="host-passthrough" check="none" migratable="on"/>
            <clock offset="utc">
                <timer name="rtc" tickpolicy="catchup"/>
                <timer name="pit" tickpolicy="delay"/>
                <timer name="hpet" present="no"/>
            </clock>
            <devices>
                <emulator>/usr/bin/qemu-system-{arch}</emulator>
                {devices_xml}
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
        """.format(
            ram_mib=self.ram_mib,
            cpu_count=self.cpu_count,
            arch=self.arch,
            chipset=self.chipset,
            firmware_tags=efi_snippet,
            devices_xml=devices_xml,
        )


class Device(Component):
    """A `Component` that needs to be initialized and destroyed, and adds a device to the libvirt XML."""

    def __init__(self, ident: str | None = None):
        super().__init__(ident=ident)
        self._hypervisor = None
        self._machine_name = None

    def create(
        self, hypervisor: libvirt.virConnect | None, machine_name: str, components: list[Component]
    ):
        self._hypervisor = hypervisor
        self._machine_name = machine_name

    def destroy(self):
        pass

    def _to_xml(self):
        raise NotImplementedError


class VM:
    """
    Define a virtual machine from a list of `Component`s.

    The machine will be given a random UUID and name (in the format 'llm_xxxxxxxx').

    Args:
        components: A list of `Component`s that define the VM. A `System` is added automatically if absent
        hypervisor_uri: The hypervisor to create the VM in (`qemu:///system` by default)

    Example:
        Creating the machine:

            # Doesn't have a disk, will be created but won't boot
            machine = VM()

            # Enough to boot, has default System() parameters
            machine = VM([Disk('example.qcow2')])

            # Machine with extra resources
            machine = VM([
                System(ram_mib=512, cpu_count=2),
                Disk('example.qcow2'),
            ])

            # Machine with alternative architecture (Not implemented)
            machine = VM([
                System(arch='arm'),
                Disk('example.qcow2'),
            ])

            # Netboot instead of disk
            machine = VM([Interface(VNet(netboot_root='/tmp/my_netboot'), netboot=True)])
    """

    _CREATE_TRIES = 10

    @staticmethod
    def pretty_format_components(components):
        """
        Return a pretty representation of the given components.

        TODO: Currently not pretty
        """
        return str(components)

    def __str__(self):
        return VM.pretty_format_components(self.components)

    def __init__(self, components: list[Component], hypervisor_uri="qemu:///system"):
        if System.of(components) is None:
            components.append(System())

        self.components = components
        self._hypervisor_uri = hypervisor_uri
        self._libvirt = None
        self._dom = None
        self.name = None
        self._uuid = None

        # if this reaches zero then the VM gets destroyed
        self._refcount = 0

        self._create()

    def leak(self):
        """Makes the current VM object not destroy the domain on garbage collection."""
        self._refcount += 1

    def _create(self):
        """Create the machine, and initialize all devices."""
        if self._hypervisor_uri not in _hypervisor_connections:
            _hypervisor_connections[self._hypervisor_uri] = libvirt.open(self._hypervisor_uri)

        self._libvirt = _hypervisor_connections[self._hypervisor_uri]

        self._refcount += 1
        if self._refcount != 1:
            return

        # Attempt to recreate VM multiple times - in case of uuid/name conflict or OOM
        for i in range(VM._CREATE_TRIES):
            try:
                self._uuid = str(uuid.uuid4())
                self.name = f"llm_{hex(random.randint(0, 0xffffffff))[2:]}"

                # Gather devices xml
                devices_xml = ""
                for device in Device.all_of(self):
                    device.create(self._libvirt, self.name, self.components)
                    devices_xml += device._to_xml()

                xml = """
                <domain type='kvm'>
                    <name>{name}</name>
                    <uuid>{uuid}</uuid>
                    {system}
                </domain>
                """.format(
                    name=self.name,
                    uuid=self._uuid,
                    system=System.of(self)._to_xml(self, devices_xml),
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
                if i == VM._CREATE_TRIES - 1:
                    raise
                time.sleep(3)
            except Exception:
                # We failed to create the VM, destroy all devices
                for device in Device.all_of(self):
                    try:
                        device.destroy()
                    except libvirt.libvirtError:
                        pass
                raise

    def destroy(self):
        """Destroy the machine and all devices."""
        if self._refcount == 0:
            return
        self._refcount -= 1
        if self._refcount <= 1:
            if self._dom:
                try:
                    self._dom.destroy()
                except libvirt.libvirtError:
                    pass

            for device in Device.all_of(self):
                try:
                    device.destroy()
                except libvirt.libvirtError:
                    pass

    def console(self):
        """Spawn a virt-manager console of the machine."""
        sp.call(
            [
                "virt-manager",
                "--connect",
                self._hypervisor_uri,
                "--show-domain-console",
                self._uuid,
            ]
        )

    def type(self, text: str) -> None:
        """Type text into the console."""
        for c in text:
            self._dom.sendKey(0, 0, [liblab.keycodes.keys[c.upper()]], 1, 0)
            time.sleep(0.05)

    def __getitem__(self, key):
        return Component.by_id(self, key)

    def __del__(self):
        self.destroy()


@dataclasses.dataclass
class DHCPLease:
    iface: str
    expiry_time: int
    type: int
    mac_addr: str
    ip_addr: str
    prefix: int
    hostname: str | None
    client_id: str | None
    iaid: str | None


class VNet:
    """
    Define a virtual network, connecting guests, the host, and (optionally) the internet together.

    Args:
        internet: Should the VM have access to the host's network (i.e. the internet)?
        netboot_root: Make the DHCP server host a PXE+TFTP server and serve an the given directory
        netboot_file: Which file inside the `netboot_root` should be the main boot file (`pxelinux.0` by default)
        hypervisor_uri: The hypervisor to create the network in (`qemu:///system` by default)

    Example:
        Two machines in a network:

            net = VNet()
            vm1 = VM([SATADisk('example.qcow2'), E1000Interface(net)])
            vm2 = VM([SATADisk('example.qcow2'), E1000Interface(net)])

        Network with PXE (netboot) server:

            net = VNet(netboot_root='/tmp/my_netboot')
    """

    _CREATE_TRIES = 10

    def __init__(
        self,
        internet=False,
        netboot_root=None,
        netboot_file="pxelinux.0",
        hypervisor_uri="qemu:///system",
    ):
        self._internet = internet
        self._netboot_root = netboot_root
        self._netboot_file = netboot_file
        self._hypervisor_uri = hypervisor_uri
        self._libvirt = None
        self._net = None
        self._uuid = None
        self.name = None

        # if this reaches zero then the network gets destroyed
        self._refcount = 0

        self._create()

    def leak(self):
        """Makes the current VNet object not destroy the network on garbage collection."""
        self._refcount += 1

    def attach_interface(self, iface):
        sp.call(["ip", "link", "set", "dev", iface, "master", self.name])

    def _create(self):
        """Create the network."""
        if self._hypervisor_uri not in _hypervisor_connections:
            _hypervisor_connections[self._hypervisor_uri] = libvirt.open(self._hypervisor_uri)

        self._libvirt = _hypervisor_connections[self._hypervisor_uri]

        self._refcount += 1
        if self._refcount != 1:
            return

        # Get existing system routes, so we don't conflict with them
        routes = [route["dst"] for route in json.loads(sp.check_output(["ip", "--json", "route"]))]

        # Attempt to recreate VNet multiple times - in case of uuid/name conflict or OOM
        for i in range(VNet._CREATE_TRIES):
            try:
                self._uuid = str(uuid.uuid4())
                self.name = f"lln_{hex(random.randint(0, 0xffffffff))[2:]}"

                oct1 = random.randint(0, 254)
                oct2 = random.randint(0, 254)

                if any(_subnets_intersect(route, f"10.{oct1}.{oct2}.0/24") for route in routes):
                    raise ValueError("Subnet conflict")

                # no-ping: by default dnsmasq (the dhcp server) sends an arping and an icmp ping to
                #          an ip before giving it out. since we control the network there's no need
                #          for that. This speeds up boot by ~3 secs.
                xml = f"""
                <network xmlns:dnsmasq='http://libvirt.org/schemas/network/dnsmasq/1.0'>
                    <name>{self.name}</name>
                    <uuid>{self._uuid}</uuid>
                    <bridge name="{self.name}" stp="off" delay="0"/>
                    {'<forward mode="nat"/>' if self._internet else ''}
                    <ip address="10.{oct1}.{oct2}.1" netmask="255.255.255.0">
                        {f'<tftp root="{self._netboot_root}"/>' if self._netboot_root else ''}
                        <dhcp>
                            <range start="10.{oct1}.{oct2}.2" end="10.{oct1}.{oct2}.254"/>
                            {f'<bootp file="{self._netboot_file}"/>' if self._netboot_root else ''}
                        </dhcp>
                    </ip>
                    <dnsmasq:options>
                        <dnsmasq:option value="no-ping"/>
                    </dnsmasq:options>
                </network>
                """

                # Create the network
                self._net = self._libvirt.networkCreateXML(xml)
                break
            except libvirt.libvirtError as e:
                # Retry if it's not the last iteration
                if i == VNet._CREATE_TRIES - 1:
                    raise
                if isinstance(e, libvirt.libvirtError):
                    time.sleep(3)

    @property
    def dhcp_leases(self) -> list[DHCPLease]:
        """
        Get a dictionary of DHCP leases on the network.

        Example:
            net = VNet()
            print(net.dhcp_leases)
        """
        if not self._net:
            return []

        leases = []
        for lease in self._net.DHCPLeases():
            leases.append(
                DHCPLease(
                    iface=lease["iface"],
                    expiry_time=lease["expirytime"],
                    type=lease["type"],
                    mac_addr=lease["mac"],
                    ip_addr=lease["ipaddr"],
                    prefix=lease["prefix"],
                    hostname=lease["hostname"],
                    client_id=lease["clientid"],
                    iaid=lease["iaid"],
                )
            )
        return leases

    def wireshark(self, capture_filter=None, display_filter=None):
        args = ["wireshark", "-n", "-l", "-k", "-i", self.name]
        if capture_filter:
            args += ["-f", capture_filter]
        if display_filter:
            args += ["-Y", display_filter]
        sp.Popen(args, stdout=sp.DEVNULL, stderr=sp.DEVNULL)

    def destroy(self):
        """Destroy the network."""
        if self._refcount == 0:
            return
        self._refcount -= 1
        if self._refcount <= 1 and self._net:
            try:
                self._net.destroy()
            except libvirt.libvirtError:
                pass

    def __del__(self):
        self.destroy()


def _subnets_intersect(a: str, b: str) -> bool:
    subnet_ranges = []
    for subnet in (a, b):
        if subnet.count("/") != 1:
            return False
        ip, mask = subnet.split("/")
        rev_mask = 0xFFFFFFFF >> int(mask)
        ip = struct.unpack(">I", bytes(int(octet) for octet in ip.split(".")))[0]
        subnet_ranges.append((ip & ~rev_mask, ip | rev_mask))

    return (
        subnet_ranges[0][0] <= subnet_ranges[1][1] and subnet_ranges[0][1] >= subnet_ranges[1][0]
    )
