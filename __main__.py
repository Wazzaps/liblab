from vm import VM, SATADisk

if __name__ == '__main__':
    with VM([SATADisk('example.qcow2')]) as machine:
        machine.console()
        input('Press enter to kill VM. (All changes will be lost!)')
