#!/usr/bin/python

"""
/*
* This program is free software; you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation; either version 2 of the License, or
* (at your option) any later version.
*
*   device_database.py
*   Naredula Janardhana Reddy  (naredula.jana@gmail.com, naredula.jana@yahoo.com)
*
*/
"""

device_list = []
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
device_list.append([])
# [name, size, number of elements, version] from 1 to n
# [name ,0, size, version] for the first element 
# The below are Hardcoded sizes for qemu 1.6.1, By changing the snapshot file format, this harcoding can be removed.
VIRTIO_NET_DEV_SIZE = 944
VIRTIO_PCI_SIZE = 327
CPU_SIZE = 1817
PIIX4_PM_SIZE = 312
IDE_SIZE = 1966
FDC_SIZE = 593
DMA_SIZE = 75
VMMOUSE_SIZE = 4105
PCKBD_SIZE = 4
PS2_MOUSE_SIZE = 291
PS2_KBD_SIZE = 284
SERIAL_SIZE = 11
I8254_SIZE = 108
HPET_SIZE = 151
CIRRUSVGA_SIZE = 1870
FWCFG_SIZE = 6
PCIBUS_SIZE = 20
I440FX_SIZE = 277
PIIX3_SIZE = 292
E1000_SIZE = 67608  # 67640-32
"""
strings -a -t d /data/vmm_qemu/qemu_1.5.1/bin/S | grep e1000

device entries:  name , size, version,
"""
device_list[0]=[['timer',0,0,2,0],['cpu_ticks_offset' , 8, 0, 0, 0],['dummy' , 8, 0, 0, 24],['cpu_clock_offset' , 8, 0, 2, 8]]
# total length = 24 
device_list[1]=[['block',0,0,1,0]]
device_list[2]=[['ram',0,0,4,0]]
device_list[3]=[['cpu_common',0,0,1,0],['halted' , 4, 0, 0, 0],['interrupt_request' , 4, 0, 0, -48]]
# total length = 8 
device_list[4]=[['cpu',0,CPU_SIZE,12,0],['env.regs' , 8, 16, 0, 0],['env.eip' , 8, 0, 0, 128],['env.eflags' , 8, 0, 0, 136],['env.hflags' , 4, 0, 0, 176],['env.fpuc' , 2, 0, 0, 474],['env.fpus_vmstate' , 2, 0, 0, 66888],['env.fptag_vmstate' , 2, 0, 0, 66890],['env.fpregs_format_vmstate' , 2, 0, 0, 66892],['env.fpregs' , 16, 8, 0, 496],['env.fpregs' , 16, 8, 0, 496],['env.fpregs' , 16, 8, 0, 496],['env.segs' , 24, 6, 0, 184],['env.ldt' , 24, 0, 0, 328],['env.tr' , 24, 0, 0, 352],['env.gdt' , 24, 0, 0, 376],['env.idt' , 24, 0, 0, 400],['env.sysenter_cs' , 4, 0, 0, 976],['env.sysenter_esp' , 8, 0, 0, 984],['env.sysenter_eip' , 8, 0, 0, 992],['env.sysenter_esp' , 8, 0, 7, 984],['env.sysenter_eip' , 8, 0, 7, 992],['env.cr[0]' , 8, 0, 0, 448],['env.cr[2]' , 8, 0, 0, 464],['env.cr[3]' , 8, 0, 0, 472],['env.cr[4]' , 8, 0, 0, 480],['env.dr' , 8, 8, 0, 1192],['env.a20_mask' , 4, 0, 0, 464],['env.mxcsr' , 4, 0, 0, 688],['env.xmm_regs' , 16, 16, 0, 696],['env.efer' , 8, 0, 0, 1000],['env.star' , 8, 0, 0, 1008],['env.lstar' , 8, 0, 0, 1064],['env.cstar' , 8, 0, 0, 1072],['env.fmask' , 8, 0, 0, 1080],['env.kernelgsbase' , 8, 0, 0, 1088],['env.smbase' , 4, 0, 4, 1288],['env.pat' , 8, 0, 5, 66152],['env.hflags2' , 4, 0, 5, 180],['parent_obj.halted' , 4, 0, 0, -4],['env.vm_hsave' , 8, 0, 5, 1016],['env.vm_vmcb' , 8, 0, 5, 1024],['env.tsc_offset' , 8, 0, 5, 1032],['env.intercept' , 8, 0, 5, 1040],['env.intercept_cr_read' , 2, 0, 5, 1048],['env.intercept_cr_write' , 2, 0, 5, 1050],['env.intercept_dr_read' , 2, 0, 5, 1052],['env.intercept_dr_write' , 2, 0, 5, 1054],['env.intercept_exceptions' , 4, 0, 5, 1056],['env.v_tpr' , 1, 0, 5, 1060],['env.mtrr_fixed' , 8, 11, 8, 66272],['env.mtrr_deftype' , 8, 0, 8, 66360],['env.mtrr_var' , 16, 8, 8, 66368],['env.interrupt_injected' , 4, 0, 9, 66504],['env.mp_state' , 4, 0, 9, 66496],['env.tsc' , 8, 0, 9, 1136],['env.exception_injected' , 4, 0, 11, 66500],['env.soft_interrupt' , 1, 0, 11, 66508],['env.nmi_injected' , 1, 0, 11, 1296],['env.nmi_pending' , 1, 0, 11, 1297],['env.has_error_code' , 1, 0, 11, 66509],['env.sipi_vector' , 4, 0, 11, 66512],['env.mcg_cap' , 8, 0, 10, 66544],['env.mcg_status' , 8, 0, 10, 1160],['env.mcg_ctl' , 8, 0, 10, 66552],['env.mce_banks' , 8, 40, 10, 66560],['env.tsc_aux' , 8, 0, 11, 66880],['env.system_time_msr' , 8, 0, 11, 1096],['env.wall_clock_msr' , 8, 0, 11, 1104],['env.xcr0' , 8, 0, 12, 67160],['env.xstate_bv' , 8, 0, 12, 66896],['env.ymmh_regs' , 16, 16, 12, 66904]]
# total length = 2333 
device_list[5]=[['kvm-tpr-opt',0,0,1,0],['rom_state' , 124, 0, 0, 0],['state' , 4, 0, 0, -20],['real_tpr_addr' , 4, 0, 0, -4],['rom_state_vaddr' , 4, 0, 0, -12],['vapic_paddr' , 4, 0, 0, -8],['rom_state_paddr' , 4, 0, 0, -16]]
# total length = 144 
device_list[6]=[['apic',0,0,3,0],['apicbase' , 4, 0, 0, 0],['id' , 1, 0, 0, 4],['arb_id' , 1, 0, 0, 5],['tpr' , 1, 0, 0, 6],['spurious_vec' , 4, 0, 0, 8],['log_dest' , 1, 0, 0, 12],['dest_mode' , 1, 0, 0, 13],['isr' , 4, 8, 0, 16],['tmr' , 4, 8, 0, 48],['irr' , 4, 8, 0, 80],['lvt' , 4, 6, 0, 112],['esr' , 4, 0, 0, 136],['icr' , 4, 2, 0, 140],['divide_conf' , 4, 0, 0, 148],['count_shift' , 4, 0, 0, 152],['initial_count' , 4, 0, 0, 156],['initial_count_load_time' , 8, 0, 0, 160],['next_time' , 8, 0, 0, 168],['timer_expiry' , 8, 0, 0, 192]]
# total length = 201 
device_list[7]=[['kvmclock',0,0,1,0],['clock' , 8, 0, 0, 0]]
# total length = 8 
device_list[8]=[['fw_cfg',0,FWCFG_SIZE,2,0],['cur_entry' , 2, 0, 0, 0],['cur_offset' , 4, 0, 0, 4],['cur_offset' , 4, 0, 2, 4]]
# total length = 10 
device_list[9]=[['PCIBUS',0,PCIBUS_SIZE,1,0],['nirq' , 4, 0, 0, 0],['irq_count' , 4, 0, 0, 8]]
# total length = 8 
device_list[10]=[['/I440FX',0,I440FX_SIZE,3,0],['dev' , 1704, 0, 0, 0],['smm_enabled' , 1, 0, 0, 11512]]
# total length = 1705 
device_list[11]=[['/PIIX3',0,PIIX3_SIZE,3,0],['dev' , 1704, 0, 0, 0],['pci_irq_levels_vmstate' , 4, 4, 3, 1720]]
# total length = 1724 
device_list[12]=[['i8259',0,0,1,0],['last_irr' , 1, 0, 0, 0],['irr' , 1, 0, 0, 1],['imr' , 1, 0, 0, 2],['isr' , 1, 0, 0, 3],['priority_add' , 1, 0, 0, 4],['irq_base' , 1, 0, 0, 5],['read_reg_select' , 1, 0, 0, 6],['poll' , 1, 0, 0, 7],['special_mask' , 1, 0, 0, 8],['init_state' , 1, 0, 0, 9],['auto_eoi' , 1, 0, 0, 10],['rotate_on_auto_eoi' , 1, 0, 0, 11],['special_fully_nested_mode' , 1, 0, 0, 12],['init4' , 1, 0, 0, 13],['single_mode' , 1, 0, 0, 14],['elcr' , 1, 0, 0, 15]]
# total length = 16 
device_list[13]=[['ioapic',0,0,3,0],['id' , 1, 0, 0, 0],['ioregsel' , 1, 0, 0, 1],['unused' , 8, 0, 2, -9176],['irr' , 4, 0, 2, 4],['ioredtbl' , 8, 24, 0, 8]]
# total length = 214 
device_list[14]=[['/cirrus_vga',0,CIRRUSVGA_SIZE,2,0],['dev' , 1704, 0, 0, 0],['cirrus_vga' , 77488, 0, 0, 1704]]
# total length = 79192 
device_list[15]=[['hpet',0,HPET_SIZE,2,0],['config' , 8, 0, 0, 0],['isr' , 8, 0, 0, 8],['hpet_counter' , 8, 0, 0, 16],['num_timers' , 1, 0, 2, -2064],['timer' , 64, 0, 0, -2056]]
# total length = 89 
device_list[16]=[['mc146818rtc',0,0,3,0],['cmos_data' , 128, 0, 0, 0],['cmos_index' , 1, 0, 0, 128],['unused' , 28, 0, 0, -336],['periodic_timer' , 8, 0, 0, 184],['next_periodic_time' , 8, 0, 0, 192],['unused' , 24, 0, 0, -336],['irq_coalesced' , 4, 0, 2, 220],['period' , 4, 0, 2, 224],['base_rtc' , 8, 0, 3, 136],['last_update' , 8, 0, 3, 144],['offset' , 8, 0, 3, 152],['update_timer' , 8, 0, 3, 200],['next_alarm_time' , 8, 0, 3, 208]]
# total length = 245 
device_list[17]=[['i8254',0,I8254_SIZE,3,0],['channels[0].irq_disabled' , 4, 0, 3, 0],['channels' , 56, 3, 2, -48],['channels[0].next_transition_time' , 8, 0, 0, -24]]
# total length = 236 
device_list[18]=[['serial',0,SERIAL_SIZE,3,0],['state' , 328, 0, 0, 0]]
# total length = 328 
device_list[19]=[['ps2kbd',0,PS2_KBD_SIZE,3,0],['common' , 288, 0, 0, 0],['scan_enabled' , 4, 0, 0, 288],['translate' , 4, 0, 0, 292],['scancode_set' , 4, 0, 3, 296]]
# total length = 300 
device_list[20]=[['ps2mouse',0,PS2_MOUSE_SIZE,2,0],['common' , 288, 0, 0, 0],['mouse_status' , 1, 0, 0, 288],['mouse_resolution' , 1, 0, 0, 289],['mouse_sample_rate' , 1, 0, 0, 290],['mouse_wrap' , 1, 0, 0, 291],['mouse_type' , 1, 0, 0, 292],['mouse_detect_state' , 1, 0, 0, 293],['mouse_dx' , 4, 0, 0, 296],['mouse_dy' , 4, 0, 0, 300],['mouse_dz' , 4, 0, 0, 304],['mouse_buttons' , 1, 0, 0, 308]]
# total length = 307 
device_list[21]=[['pckbd',0,PCKBD_SIZE,3,0],['kbd' , 56, 0, 0, 0]]
# total length = 56 
device_list[22]=[['vmmouse',0,VMMOUSE_SIZE,0,0],['queue_size' , 4, 0, 0, 0],['queue' , 4, 1024, 0, -4096],['nb_queue' , 2, 0, 0, 4],['status' , 2, 0, 0, 6],['absolute' , 1, 0, 0, 8]]
# total length = 4109 
device_list[23]=[['port92',0,0,1,0],['outport' , 1, 0, 0, 0]]
# total length = 1 
device_list[24]=[['dma',0,DMA_SIZE,1,0],['command' , 1, 0, 0, 0],['mask' , 1, 0, 0, 1],['flip_flop' , 1, 0, 0, 2],['dshift' , 4, 0, 0, 3],['regs' , 40, 4, 1, 7]]
# total length = 207 
device_list[25]=[['fdc',0,FDC_SIZE,2,0],['state' , 336, 0, 0, 0]]
# total length = 336 
device_list[26]=[['/ide',0,IDE_SIZE,3,0],['dev' , 1704, 0, 0, 0],['bmdma' , 504, 2, 0, 5832],['bus' , 2064, 2, 1, 1704],['bus[0].ifs' , 952, 2, 3, 1824],['bus[1].ifs' , 952, 2, 3, 3888]]
# total length = 15120 
device_list[27]=[['i2c_bus',0,0,1,0],['saved_address' , 1, 0, 0, 0]]
# total length = 1 
device_list[28]=[['/piix4_pm',0,PIIX4_PM_SIZE,3,0],['dev' , 1704, 0, 0, 0],['ar.pm1.evt.sts' , 2, 0, 0, 2808],['ar.pm1.evt.en' , 2, 0, 0, 2810],['ar.pm1.cnt.cnt' , 2, 0, 0, 3000],['apm' , 200, 0, 0, 3032],['ar.tmr.timer' , 8, 0, 0, 2408],['ar.tmr.overflow_time' , 8, 0, 0, 2592],['ar.gpe' , 24, 0, 2, 2608],['pci0_status' , 8, 0, 2, 3536]]
# total length = 1958 
device_list[29]=[['/virtio-net',0,VIRTIO_NET_DEV_SIZE,11,0]]
device_list[30]=[['/virtio-balloon',0,0,1,0]]
device_list[31]=[['/e1000',0,E1000_SIZE,2,0],['parent_obj' , 1968, 0, 0, 0],['unused' , 4, 0, 0, 0],['unused' , 4, 0, 0, 0],['rxbuf_size' , 4, 0, 0, 141848],['rxbuf_min_shift' , 4, 0, 0, 141852],['eecd_state.val_in' , 4, 0, 0, 207684],['eecd_state.bitnum_in' , 2, 0, 0, 207688],['eecd_state.bitnum_out' , 2, 0, 0, 207690],['eecd_state.reading' , 2, 0, 0, 207692],['eecd_state.old_eecd' , 4, 0, 0, 207696],['tx.ipcss' , 1, 0, 0, 207660],['tx.ipcso' , 1, 0, 0, 207661],['tx.ipcse' , 2, 0, 0, 207662],['tx.tucss' , 1, 0, 0, 207664],['tx.tucso' , 1, 0, 0, 207665],['tx.tucse' , 2, 0, 0, 207666],['tx.paylen' , 4, 0, 0, 207672],['tx.hdr_len' , 1, 0, 0, 207668],['tx.mss' , 2, 0, 0, 207670],['tx.size' , 2, 0, 0, 207656],['tx.tso_frames' , 2, 0, 0, 207676],['tx.sum_needed' , 1, 0, 0, 207658],['tx.ip' , 1, 0, 0, 207679],['tx.tcp' , 1, 0, 0, 207680],['tx.header' , 256, 0, 0, 141856],['tx.data' , 65536, 0, 0, 142120],['eeprom_data' , 2, 64, 0, 141720],['phy_reg' , 2, 32, 0, 141656],['mac_reg[CTRL]' , 4, 0, 0, 10584],['mac_reg[EECD]' , 4, 0, 0, 10600],['mac_reg[EERD]' , 4, 0, 0, 10604],['mac_reg[GPRC]' , 4, 0, 0, 27084],['mac_reg[GPTC]' , 4, 0, 0, 27096],['mac_reg[ICR]' , 4, 0, 0, 10776],['mac_reg[ICS]' , 4, 0, 0, 10784],['mac_reg[IMC]' , 4, 0, 0, 10800],['mac_reg[IMS]' , 4, 0, 0, 10792],['mac_reg[LEDCTL]' , 4, 0, 0, 14168],['mac_reg[MANC]' , 4, 0, 0, 33144],['mac_reg[MDIC]' , 4, 0, 0, 10616],['mac_reg[MPC]' , 4, 0, 0, 26984],['mac_reg[PBA]' , 4, 0, 0, 14680],['mac_reg[RCTL]' , 4, 0, 0, 10840],['mac_reg[RDBAH]' , 4, 0, 0, 20828],['mac_reg[RDBAL]' , 4, 0, 0, 20824],['mac_reg[RDH]' , 4, 0, 0, 20840],['mac_reg[RDLEN]' , 4, 0, 0, 20832],['mac_reg[RDT]' , 4, 0, 0, 20848],['mac_reg[STATUS]' , 4, 0, 0, 10592],['mac_reg[SWSM]' , 4, 0, 0, 33960],['mac_reg[TCTL]' , 4, 0, 0, 11608],['mac_reg[TDBAH]' , 4, 0, 0, 24924],['mac_reg[TDBAL]' , 4, 0, 0, 24920],['mac_reg[TDH]' , 4, 0, 0, 24936],['mac_reg[TDLEN]' , 4, 0, 0, 24928],['mac_reg[TDT]' , 4, 0, 0, 24944],['mac_reg[TORH]' , 4, 0, 0, 27164],['mac_reg[TORL]' , 4, 0, 0, 27160],['mac_reg[TOTH]' , 4, 0, 0, 27172],['mac_reg[TOTL]' , 4, 0, 0, 27168],['mac_reg[TPR]' , 4, 0, 0, 27176],['mac_reg[TPT]' , 4, 0, 0, 27180],['mac_reg[TXDCTL]' , 4, 0, 0, 24960],['mac_reg[WUFC]' , 4, 0, 0, 33120],['mac_reg[VET]' , 4, 0, 0, 10640],['mac_reg' , 4, 32, 0, 32088],['mac_reg' , 4, 128, 0, 31576],['mac_reg' , 4, 128, 0, 32600]]
# total length = 69320 






