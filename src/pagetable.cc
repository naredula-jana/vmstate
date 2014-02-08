/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 *   vmstate/pagetable.cc
 *   Author: Naredula Janardhana Reddy  (naredula.jana@gmail.com, naredula.jana@yahoo.com)
 *
 */

#define addr_t unsigned long
/* pde_t represents l2 directory
 Flags bits: only * are used for now
 *0 - present bit
 *1 - R/W bit
 2- U/S
 3- PWT
 4-PCD
 5- Access bit
 6- Dirty bit (ignored for 4k page)
 *7- Page size 0-for 4k 1-for 2M
 *8- Global bit (ignored for 4k page)
 12-PAT
 */
typedef struct __pde {
	addr_t present :1; // Page present in memory
	addr_t rw :1; // Read-only if clear, readwrite if set
	addr_t user :1; // Supervisor level only if clear
	addr_t pwt :1;addr_t pcd :1;addr_t accessed :1; // Has the page been accessed since last refresh?
	addr_t dirty :1; // Has the page been written to since last refresh? ignored for 2M
	addr_t ps :1; // page size 2M=1 4k=0
	addr_t global :1; // ignored in 4k
	addr_t avl :3; // available
	/*    addr_t pat	  :1 ; */
	/*  unsigned flags      :12; */
	addr_t frame :40;addr_t count :11;addr_t nx :1;
}__attribute__((packed)) pde_t;
int pte_count=0;
void put_virtual_addr(int l4,int l3, int l2, int l1, unsigned long paddr, int psize){
	unsigned long vaddr = (l4<<39)+(l3<<30)+(l2<<21) +(l1<<12) ;
#if 1
	merge_program_section(paddr,vaddr,psize);
#endif
	printf("L4-L1; %x:%x:%x:%x vaddr:%x paddr:%x ",l4,l3,l2,l1,vaddr,paddr);
	return;
}

unsigned char pg_level1[PAGE_SIZE];
int generate_level1_table(unsigned long pdt,int level4,int level3, int level2){
	int i;
	int file_offset = get_file_offset(pdt);
	pde_t *pg_table=(pde_t *)&pg_level1[0];
	memcpy(pg_table,phy_mem+file_offset,PAGE_SIZE);
	for (i=0; i<PAGE_SIZE/sizeof(pde_t); i++){
		if (pg_table->present != 0) {
			pte_count++;
			printf("  	     leve1:%x pres:%x rw:%x user:%x ps:%x global:%x frame:%x count:%x ",pte_count,pg_table->present, pg_table->rw, pg_table->user,
					pg_table->ps, pg_table->global,pg_table->frame,pg_table->count);

			put_virtual_addr(level4,level3,level2,i,pg_table->frame*0x1000, PAGE_SIZE);
			printf("\n");
		}
		pg_table++;
	}
}

unsigned char pg_level2[PAGE_SIZE];
int generate_level2_table(unsigned long pdt,int level4, int level3){
	int i;
	int file_offset = get_file_offset(pdt);
	pde_t *pg_table=(pde_t *)&pg_level2[0];
	memcpy(pg_table,phy_mem+file_offset,PAGE_SIZE);
	for (i=0; i<PAGE_SIZE/sizeof(pde_t); i++){
		if (pg_table->present != 0) {
			printf("  	  leve2: pres:%x rw:%x user:%x ps:%x global:%x frame:%x count:%x  \n",pg_table->present, pg_table->rw, pg_table->user,
					pg_table->ps, pg_table->global,pg_table->frame,pg_table->count);
			if (pg_table->ps == 1){ /* 2M page */
				int k;
				for (k=0; k<512; k++)
					put_virtual_addr(level4,level3,i,k,pg_table->frame*0x1000 + (k*0x1000), PAGE_SIZE);
			}else{
				generate_level1_table(pg_table->frame*0x1000,level4,level3,i);
			}
		}
		pg_table++;
	}
}

unsigned char pg_level3[PAGE_SIZE];
int generate_level3_table(unsigned long pdt, int level4){
	int i;
	int file_offset = get_file_offset(pdt);
	pde_t *pg_table=(pde_t *)&pg_level3[0];
	memcpy(pg_table,phy_mem+file_offset,PAGE_SIZE);
	for (i=0; i<PAGE_SIZE/sizeof(pde_t); i++){
		if (pg_table->present != 0) {
			printf("  leve3: pres:%x rw:%x user:%x ps:%x global:%x frame:%x count:%x  \n",pg_table->present, pg_table->rw, pg_table->user,
					pg_table->ps, pg_table->global,pg_table->frame,pg_table->count);
			generate_level2_table(pg_table->frame*0x1000,level4,i);
		}
		pg_table++;
	}
}
unsigned char pagetable[PAGE_SIZE];
int generate_virtual_addrs(unsigned long cr3, unsigned char *corefile){
	int i;
	int file_offset = get_file_offset(cr3);
	pde_t *pg_table=(pde_t *)&pagetable[0];
	memcpy(pg_table,phy_mem+file_offset,PAGE_SIZE);
	for (i=0; i<PAGE_SIZE/sizeof(pde_t); i++){
		if (pg_table->present != 0){
			printf("pres:%x rw:%x user:%x ps:%x global:%x frame:%x  \n",pg_table->present, pg_table->rw, pg_table->user,
				pg_table->ps, pg_table->global,pg_table->frame,pg_table->count);
			generate_level3_table(pg_table->frame*0x1000,i);
		}
		pg_table++;
	}

	adjust_program_headers();
	generate_elf(corefile);
}

