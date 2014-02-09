#Vmstate:#
    -Tool to Analyse and Modify virtual machine state

  Virtual machine state  is the state of software and hardware in the virtual machine, means state of pysical memory,cpu,NIC and other devices etc. Virtual machine Snapshot from hypervisor(qemu) is one form of virtual machine(vm) state, Snapshot not only  be used for Live migration, It can also be used by system programmers to analyze software and hardware running in the virtual machine. In this paper vmstate tool will be explained, and how the tool can used to analyze and modify the state for trouble shooting the hardware and software of the virtual machine.  
  
**Key difference between virtual and physical:** It is easy and reliable to capture the virtual machine state when compare to the physical machine.  The key difference is, in the vm the state is captured from outside, where as in the physical machine the state is captured from inside. due to this it will be difficult to capture the state, state like partial kernel core and application cores can be captured in the physical memory from inside. 

**Flow :  Steps to analysis and modify virtual machine from outside**:
The following is the flow of machine state conversion  from one format to another. vm is converted in to a passive file called snapshot, usually the snapshot is created by the hypervisor for migrating the vm from one host to another. But here we are using for analysis and modification purpose. This snapshot is converted in to software specific core dumpfile and hardware related device file(xml file), these files are created by vmstate tool.  The state is analyzed , modified and re-injected back in to the snapshot by the vmstate tool. The modified snapshot is again converted in to vm by the hypervisor. The new vm will start continuing to run from the point where it as been stopped before the state is captured. 
 
  vm-->snapshot-->{Hs+Ss}-->{newHs+newSs}-->newSnapshot-->newVm
 
 -  Hs/newHs : old and new Hardware state ([example file](https://github.com/naredula-jana/vmstate/blob/master/bin/file_devicestate.xml)). These files are created  by vmstate tool.
 -  Ss/newSs : software state in core dump file format interpreted by gdb, created by vmstate tool.
 -  snapshot/newSnapshot : Snapshot is a vm in a passive format. created/consumed by hypervisor. 
 -  vm/newVm : old and new VM will have almost the same state except the changes done by the user using vmstate tool.

**Hypervisor(qemu+kvm)** : converts from active virtual machine(vm) to a passive snapshot format, and viceversa.
**vmstate tool**: It is used for the following  three purposes:
1. Extract  hardware(Hs) + software(Ss) states of vm  from the snapshot.
2. Modify/edit the  software/hardware states using gdb aswell as vmstate tool. 
3. Re-inject the modified Hardware+software states back to snapshot format.


#Example Usecase:#
 
 Suppose we want to change the MAC address of a running virtual machine for some experiments. If we want to do the samething on a physical machine, we may not achieve it, we can at the maximum connect the live debugger and modify the kernel memory to reflect the change of MAC address in software but not hardware. The following steps show how it is acheived in virtual machine using the vmstate tool.

1. **Stop vm and create Snapshot**:stop the vm, and  capture the vm snapshot from qemu.
2. **Generate software(Ss) and hardware states(Hs) from snapshot**: use vmstate tool to generate kernel core dump file(software state) and device state file(hardware state)
3. **Modify software state(newSs)**:modify kernel core file to change the MAC address at various places using gdb.
4. **Modify hardware state(newHs)**:modify device file , to change the mac address in NIC.
5. **Inject the state changes to  snapshot**: add the changes of kernel core file and modified device file into snapshot using vmstate tool. This will create a new snapshot file.
6. **Recreate the vm from new snapshot**: continue or activate the VM using the new snapshot file created from step-5. vm will start running from the point where it is stopped in step-1 but with the new MAC address inside the NIC and inside the OS.

step-3 to step-6 can be repeated till the desired result is achieved. This is not possible in physical machine because we are directly working on the state without backing the orginal state and also the hardware is running. In the case of vm, even if the do not get the desired result in step-6, the orginal state of the vm is preserved in step-1, so we can loop back from step-3 to step-6 again.   

#Differences of machine state on a Metal versus Virtual:#
The state capture of application,kernel and device  will be consistent and easy in virtual environment(vm) when compare to the metal(physical machine):

 1. **Application core**: The quality and complexity in generation of core dump will be similar in both metal aswell as virtual.
 2. **kernel core dump**:  
   - On the metal, getting the kernel dump during early kernel boot stage is not possible.On a SMP machine it will be difficult, since it need to be capture from inside the running OS. 
  - But in the VM, the kernel core can be captured consistently in all possible conditions ,  since it is captured from outside by stopping the machine for a while, so it will consistent and relatively lot easy. 
 3. **Device state**: On a metal it is very difficult or it may not be possible to capture the state of the device like(eg NIC etc), since the devices can not be frozen/stopped. 
 4. **Within a machine**: device, kernel and application, all the three can be captured at one shot, this is almost impossible on the metal without any external hardware help. 
 5. **Across the machines: cluster of machines or a group of machines inside a chassis**: To captures the state of all the machine in a cluster or chassis at one shot is very difficult in metal. This will easy in virtual environment by broadcasting a message(udp packet) to all the hypervisors, so as hypervisors will trigger the snapshot or state capture with a slight time difference from machine to machine. 


In the Virtual environment, all the vm's can be stopped momentarily and can take the snapshot. These snapshots are used to extract  the state of devices , kernel and applications core dumps to full extent. Vmstate project is to extract all the required data from the snapshot generated by qemu and convert in to ELF core format that can be interpreted by the GDB.

Software inside the vm can trigger the signal to the orchestration layer like openstack/cloudstack that can capture the snapshot from hypervisor. The signal can also be deliver using the para virtual drivers like memballoning.


#Vmstate tool Status:#

**Completed:**

 1. generating x86_64 kernel cores for [Jiny OS](https://github.com/naredula-jana/Jiny-Kernel) and other kernels like linux/freebsd.
 - generating partial device state.
 
 

**TODO:**

  1. Re-injecting the modified software+Hardware state in to the orginal Snapshot to  create a new snapshot or new vm . 
  2. Kernel/app core dumps for platforms other then amd64(x86_64).
  - Core dump for the app inside the Jiny/frebsd/linux.(in progress)
  - Detailed device state capture.
  - finding a procedure to send the signal to hypervisor from the guest os to capture the snapshot.
  - storing more data in the snapshot by the hypervisor.


#Related Projects:#
 -[Jiny OS](https://github.com/naredula-jana/Jiny-Kernel): Thin kernel for Virtualization.
 
 