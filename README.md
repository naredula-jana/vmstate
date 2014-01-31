vmstate to core files
=======
  Snapshot from qemu can be used for the following apart from live or offline migration:

 - generate the  kernel core to debug the kernel state using gdb.
 - application cores  to debug application using gdb
 - devices state in details(example: virtio, cpu, memory state etc).


#Completed:#
 - generating kernel core for [Jiny OS](https://github.com/naredula-jana/Jiny-Kernel).
 - partial device state

#TODO:#
  - currently kernel core is only for Jiny, need to parse page tables to capture for any kernel like freebsd,linux.
  - cores for the app(inside the Jiny).
  - Indetail device state capture.