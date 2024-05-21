"""Storage and images"""

import os.path
import string
import subprocess as sp

from liblab.vm import Device


class SATADisk(Device):
    """
    A SATA storage device backed by a QCow2 image, and linked-cloned by default.

    "Disk" is an alias for "SATADisk".

    Example:
        Create a linked clone disk:

            Disk('example.qcow2')

        Create a live disk (All changes made in VM are saved):

            Disk('example.qcow2', linked_clone=False)
    """

    _LINKED_CLONES_DIR = "/tmp/liblab_disks"

    def __init__(self, image_path, linked_clone=True, ident=None):
        assert image_path.endswith(".qcow2"), "Images must be QCow2"
        super().__init__(ident=ident)
        self.image_path = os.path.abspath(image_path)
        self._linked_clone = linked_clone
        self.idx_in_machine = None
        self.live_image_path = None

    @staticmethod
    def _create_linked_clone(image_path, clone_name):
        assert os.path.exists(image_path), f"Disk image not found: {image_path}"
        clone_path = os.path.join(Disk._LINKED_CLONES_DIR, clone_name)
        assert not os.path.exists(
            clone_path
        ), f"Linked clone name conflict: {clone_path} (when creating clone of: {image_path})"
        if not os.path.exists(Disk._LINKED_CLONES_DIR):
            os.mkdir(Disk._LINKED_CLONES_DIR)

        sp.check_output(["qemu-img", "create", "-f", "qcow2", "-b", image_path, clone_path])

        return clone_path

    def __str__(self):
        if self._linked_clone:
            return f"{type(self).__name__}(base={repr(self.image_path)}, clone={repr(self.live_image_path)})"
        else:
            return f"{type(self).__name__}({repr(self.image_path)})"

    def create(self, hypervisor, machine_name, components):
        self.idx_in_machine = Disk.all_of(components).index(self)
        if self._linked_clone:
            self.live_image_path = Disk._create_linked_clone(
                self.image_path, clone_name=f"{machine_name}-disk{self.idx_in_machine}.qcow2"
            )
        else:
            self.live_image_path = self.image_path

    def destroy(self):
        if self._linked_clone:
            try:
                os.unlink(self.live_image_path)
            except FileNotFoundError:
                pass

    def _to_xml(self):
        assert self.live_image_path, "Please call `Disk.create` first"
        return f"""
        <disk type='file' device='disk'>
            <driver name='qemu' type='qcow2'/>
            <source file='{self.live_image_path}'/>
            <target dev='sd{string.ascii_lowercase[self.idx_in_machine]}' bus='sata'/>
        </disk>
        """


Disk = SATADisk
