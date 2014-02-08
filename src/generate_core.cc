/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 *   vmstate/generate_core.cc
 *   Author: Naredula Janardhana Reddy  (naredula.jana@gmail.com, naredula.jana@yahoo.com)
 *
 */
extern "C" {
#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <string.h>
#include <unistd.h>

#include "elf.h"

unsigned long cr3=0;
void read_fileoffsets(unsigned char *file);

#define NON_COMPRESSEED  0xfff
typedef struct struct_mem_offset {
	unsigned long addr, offset, compress;
} mem_offset_t;
//#define DEBUG 1

#define MAX_ENTRIES 1000000
mem_offset_t phymem_offset[MAX_ENTRIES];
int total_pages = 0;
unsigned char *phy_mem;
int phy_fd;
#include "core_elf.cc"
#include "pagetable.cc"
int main(int argc, char **argv) {
	struct stat stat;

	printf(" memfile :%s  input file :%s  output elf file:%s\n",argv[1],argv[2],argv[3]);

	FILE *fp = freopen ("./dbg_output", "w", stdout);

	read_fileoffsets((unsigned char *)argv[1]);

	phy_fd = open(argv[2], 0, O_RDONLY);
	fstat(phy_fd, &stat);
	phy_mem = (unsigned char *) mmap(0, stat.st_size, PROT_READ, MAP_PRIVATE,
			phy_fd, 0);
	printf(" size of the vmstate file :%d \n", stat.st_size);

	/* busy box application in jiny cr3 - 0x3fb07000, */
//	generate_virtual_addrs(0x101000);

	generate_virtual_addrs(cr3,(unsigned char *)argv[3]); /* busy box */
	return 0;
}

void read_fileoffsets(unsigned char *file) {
	int i = 0;
	unsigned long regs[20];
	int completed=0;

	total_pages = 0;
	FILE *fd = fopen((const char *)file, "r");
	if (fd==0){
		printf(" ERROR opening the file\n");
		_exit(1);
	}
	while (total_pages < MAX_ENTRIES && !feof(fd)) {
		fscanf(fd, "%x %x %x\n", &phymem_offset[total_pages].addr,
				&phymem_offset[total_pages].offset, &phymem_offset[total_pages].compress);
		if (phymem_offset[total_pages].addr==0 && phymem_offset[total_pages].offset==0 && phymem_offset[total_pages].compress==0){
			while(!feof(fd)){
				unsigned char name[100];
				fscanf(fd, "%s ",name);
				printf(" NAME :%s:\n",name);
				if (strcmp((const char *)name,(const char *)"env.regs")==0){
					fscanf(fd, "%x %x %x %x %x %x %x %x %x %x %x %x %x %x %x %x\n",&regs[0],&regs[1],&regs[2],&regs[3],&regs[4],&regs[5],&regs[6],&regs[7],
							&regs[8],&regs[9],&regs[10],&regs[11],&regs[12],&regs[13],&regs[14],&regs[15]);
					write_regs(&regs[0]);
				}else if (strcmp((const char *)name,(const char *)"env.cr[3]")==0){
					fscanf(fd, "%x\n",&cr3);
				}
			}
			return;
		}
#ifdef DEBUG
		printf("ONE %x: %x %x %x\n", total_pages, phymem_offset[total_pages].addr,
				phymem_offset[total_pages].offset, phymem_offset[total_pages].compress);
#endif
		if (completed ==0){
			total_pages++;
		}
		if (total_pages > 1) {
			if (phymem_offset[total_pages - 1].addr
					< phymem_offset[total_pages - 2].addr) {
				total_pages--;
				completed =1;
			}
		}
	}

	return;
}

}
