vmstate to core files
=======
  Snapshot from qemu can be used to generate the  kernel core and application cores  and devices state in details.
 These core files can be open using the gdb to debug/troubleshoot kernel and applications of the vm.

#Completed:#
 -  kernel core for Jiny.

#TODO:#
  - currently kernel core is only for Jiny , need to parse page tables to capture for any kernel.
  - cores for the app(inside the Jiny).
  - indetail device state capture.