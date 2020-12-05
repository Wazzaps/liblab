from vm import VM, System, SATADisk

machine = VM([
    System(
        arch='x86_64',
        chipset='pc-q35-4.2',
        ram_mib=256,
        cpu_count=1
    ),
    SATADisk('example.qcow2'),
])

machine.create()


# time.sleep(3)
# vm.destroy()
