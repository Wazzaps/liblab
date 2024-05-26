"""Storage and images"""

import os.path
import shutil
import string
import subprocess as sp
from pathlib import Path

from liblab.vm import Device


class _BaseDisk(Device):
    """
    A storage device backed by a QCow2 image, and linked-cloned by default.

    Use one of the subclasses of this class to create a disk device.

    If `expand_disk` is specified, the disk will be expanded to the specified size. Only supported
    for linked clones. The size is a string with an optional specifier (K/M/G/T) at the end.
    """

    _LINKED_CLONES_DIR = Path("/tmp/liblab_disks")
    _BUS = None

    def __init__(self, image_path, linked_clone=True, expand_disk: str | None = None, ident=None):
        assert image_path.endswith(".qcow2"), "Images must be QCow2"
        super().__init__(ident=ident)
        self.image_path: Path = Path(os.path.abspath(image_path))
        self._linked_clone = linked_clone
        self._expand_disk = expand_disk
        self.idx_in_machine = None
        self.live_image_path: Path | None = None

    @staticmethod
    def _create_linked_clone(
        image_path: Path, clone_name: str, expand_disk: str | None = None
    ) -> Path:
        assert image_path.is_file(), f"Disk image not found: {image_path}"
        clone_path = _BaseDisk._LINKED_CLONES_DIR / clone_name
        assert (
            not clone_path.exists()
        ), f"Linked clone name conflict: {clone_path} (when creating clone of: {image_path})"
        _BaseDisk._LINKED_CLONES_DIR.mkdir(parents=True, exist_ok=True)

        args = [
            "qemu-img",
            "create",
            "-f",
            "qcow2",
            "-F",
            "qcow2",
            "-b",
            str(image_path),
            str(clone_path),
        ]
        if expand_disk is not None:
            args.append(expand_disk)
        sp.check_call(args)

        return clone_path

    def __str__(self):
        if self._linked_clone:
            return (
                f"{type(self).__name__}(base={str(self.image_path)!r}, "
                f"clone={str(self.live_image_path)!r})"
            )
        else:
            return f"{type(self).__name__}({str(self.image_path)!r})"

    def create(self, hypervisor, machine_name, components):
        self.idx_in_machine = Disk.all_of(components).index(self)
        if self._linked_clone:
            self.live_image_path = Disk._create_linked_clone(
                self.image_path,
                clone_name=f"{machine_name}-disk{self.idx_in_machine}.qcow2",
                expand_disk=self._expand_disk,
            )
        else:
            self.live_image_path = self.image_path

    def destroy(self):
        if self._linked_clone and self.live_image_path and self.live_image_path.exists():
            self.live_image_path.unlink()

    def _to_xml(self):
        assert self.live_image_path, "Please call `Disk.create` first"
        return f"""
        <disk type='file' device='disk'>
            <driver name='qemu' type='qcow2'/>
            <source file='{self.live_image_path}'/>
            <target dev='sd{string.ascii_lowercase[self.idx_in_machine]}' bus='{self._BUS}'/>
            <boot order="{self.idx_in_machine + 1}"/>
        </disk>
        """


class VirtioDisk(_BaseDisk):
    """
    A Virtio storage device backed by a QCow2 image, and linked-cloned by default.

    "Disk" is an alias for "VirtioDisk".

    Example:
        Create a linked clone disk:

            Disk('example.qcow2')

        Create a live disk (All changes made in VM are saved):

            Disk('example.qcow2', linked_clone=False)
    """

    _BUS = "virtio"


class SATADisk(_BaseDisk):
    """
    A SATA storage device backed by a QCow2 image, and linked-cloned by default.

    Example:
        Create a linked clone disk:

            SATADisk('example.qcow2')

        Create a live disk (All changes made in VM are saved):

            SATADisk('example.qcow2', linked_clone=False)
    """

    _BUS = "sata"


class NVRAMImage(Device):
    """
    A read-only storage device storing an EFI NVRAM, and linked-cloned by default.
    """

    _LINKED_CLONES_DIR = Path("/tmp/liblab_disks")

    def __init__(self, image_path: Path, linked_clone=True, ident=None):
        assert image_path.name.endswith(".fd"), "Images must end with .fd"
        super().__init__(ident=ident)
        self.image_path: Path = Path(os.path.abspath(image_path))
        self._linked_clone = linked_clone
        self.live_image_path: Path | None = None

    @staticmethod
    def _create_linked_clone(image_path: Path, clone_name: str) -> Path:
        assert image_path.is_file(), f"NVRAM image not found: {image_path}"
        clone_path = NVRAMImage._LINKED_CLONES_DIR / clone_name
        assert (
            not clone_path.exists()
        ), f"Linked clone name conflict: {clone_path} (when creating clone of: {image_path})"
        NVRAMImage._LINKED_CLONES_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy(image_path, clone_path)

        return clone_path

    def __str__(self):
        if self._linked_clone:
            return (
                f"{type(self).__name__}(base={str(self.image_path)!r}, "
                f"clone={str(self.live_image_path)!r})"
            )
        else:
            return f"{type(self).__name__}({str(self.image_path)!r})"

    def create(self, hypervisor, machine_name, components):
        if self._linked_clone:
            self.live_image_path = NVRAMImage._create_linked_clone(
                self.image_path, clone_name=f"{machine_name}-nvram.fd"
            )
        else:
            self.live_image_path = self.image_path

    def destroy(self):
        if self._linked_clone and self.live_image_path and self.live_image_path.exists():
            self.live_image_path.unlink()

    def _to_xml(self):
        return ""


Disk = VirtioDisk
