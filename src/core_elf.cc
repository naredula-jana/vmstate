/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 *   core_elf.cc
 *   Author: Naredula Janardhana Reddy  (naredula.jana@gmail.com, naredula.jana@yahoo.com)
 *
 */

#define MAX_PGRM_HDRS 5000
Elf64_Phdr phdr[MAX_PGRM_HDRS];
int total_phdrs = 1; /* first header is NOTE */
unsigned long file_offset = 0;
unsigned long max_zeropages = 0;
int zerppage_index = 0;
int write_note(int fd);
int get_note_size();
unsigned long get_file_offset(unsigned long paddr) {
	unsigned long i = paddr / 0x1000;
	i = i - 1;
	return phymem_offset[i].offset;
}
int merge_program_section(unsigned long paddr,unsigned long vaddr, int psize){
	unsigned long i = paddr / 0x1000;
	i = i - 1;
	if (i>total_pages){
		printf(" ERROR: fail to add paddr:%x vaddr:%x \n",paddr,vaddr);
		return 0;
	}
	int type = phymem_offset[i].compress;

	for (i=1; i<total_phdrs; i++){
		if (((phdr[i].p_paddr+phdr[i].p_filesz) == paddr) && ((phdr[i].p_vaddr+phdr[i].p_filesz) == vaddr ) && (phdr[i].p_offset==type)){
			phdr[i].p_filesz = phdr[i].p_filesz + psize;
			phdr[i].p_memsz = phdr[i].p_filesz;
			if ((type != NON_COMPRESSEED) && (phdr[i].p_memsz > max_zeropages)){
				max_zeropages = phdr[i].p_memsz;
			}
			return 0;
		}
	}
	if (total_phdrs > (MAX_PGRM_HDRS-5)){
		printf(" ERROR Maximum program section reached \n");
		return 1;
	}
	i = total_phdrs;
	phdr[i].p_paddr = paddr;
	phdr[i].p_vaddr = vaddr;
	phdr[i].p_filesz = psize;
	phdr[i].p_memsz = phdr[i].p_filesz;
	phdr[i].p_type = PT_LOAD;
	phdr[i].p_flags = PF_W | PF_R | PF_X;
	phdr[i].p_offset = type;
//printf("\n CREATING new entry paddr:%x vaddr:%x total:%d :%d \n",paddr,vaddr,total_phdrs,i);
	total_phdrs++;
	return 1;
}

int adjust_program_headers() {
	int i;
	unsigned long file_offset=0;

	int hdrs_size = sizeof(Elf64_Ehdr) + (total_phdrs * sizeof(Elf64_Phdr)) + get_note_size();
	file_offset = hdrs_size;
	memset(&phdr[0],0,sizeof(Elf64_Phdr));
	phdr[0].p_offset = file_offset - get_note_size();
	phdr[0].p_filesz = get_note_size();
	phdr[0].p_type = PT_NOTE;
	phdr[0].p_flags = PF_R | PF_X;
	for (i = 1; i < total_phdrs; i++) {
		if(phdr[i].p_offset == NON_COMPRESSEED){
			phdr[i].p_offset = file_offset;
			file_offset = file_offset + phdr[i].p_filesz;
		}else{
			phdr[i].p_offset =  hdrs_size; /* TODO : add zero pages */
		}

		printf(" %d: paddr: %x - vaddr:%x : offset: %d size:%x  inputfileoffset:%x\n", i,
				phdr[i].p_paddr, phdr[i].p_vaddr, phdr[i].p_offset,
				phdr[i].p_filesz, get_file_offset(phdr[i].p_paddr));
	}
	printf(" max zero pages: %x :%d\n", max_zeropages, zerppage_index);
	return 1;
}
typedef struct elf64_hdr1 {
	unsigned char e_ident[16]; /* ELF "magic number" */
	Elf64_Half e_type;
	Elf64_Half e_machine;
	Elf64_Word e_version;
	Elf64_Addr e_entry; /* Entry point virtual address */
	Elf64_Off e_phoff; /* Program header table file offset */
	Elf64_Off e_shoff; /* Section header table file offset */
	Elf64_Word e_flags;
	Elf64_Half e_ehsize;
	Elf64_Half e_phentsize;
	Elf64_Half e_phnum;
	Elf64_Half e_shentsize;
	Elf64_Half e_shnum;
	Elf64_Half e_shstrndx;
} Elf64_Ehdr1;
unsigned char temp_buf[200000];
#define PAGE_SIZE 0x1000
int generate_elf(unsigned char *corefile) {
	Elf64_Ehdr1 hdr;
	int fd;
	int i;
	int hdrs_size = sizeof(Elf64_Ehdr) + (total_phdrs * sizeof(Elf64_Phdr)) + get_note_size();

	memset(&hdr, 0, sizeof(hdr));
	strcpy((char *) hdr.e_ident, ELFMAG);
	hdr.e_ident[4] = 0x2; /* x86_64 class */
	hdr.e_ident[5] = 0x1;
	hdr.e_type = ET_CORE;
	hdr.e_version = 1;

	hdr.e_machine = EM_X86_64;
	hdr.e_phnum = total_phdrs;
	hdr.e_phentsize = sizeof(Elf64_Phdr);
	hdr.e_phoff = sizeof(Elf64_Ehdr);
	fd = open((const char *)corefile, O_WRONLY | O_CREAT, 0);
	write(fd, &hdr, sizeof(Elf64_Ehdr));
	write(fd, &phdr[0], sizeof(Elf64_Phdr) * total_phdrs);
	write_note(fd);
	for (i = 1; i < total_phdrs; i++) {
		unsigned char *p = phy_mem;
		unsigned long offset;
		if (i != 1 && phdr[i].p_offset == hdrs_size)
			continue; /* skip compressed pages */
		//offset = lseek(phy_fd, 0, SEEK_CUR);
		printf(" %d: %x - %x : offset: %d size:%x  inputfileoffset:%x current offset:%x\n",
				i, phdr[i].p_paddr, phdr[i].p_vaddr, phdr[i].p_offset,
				phdr[i].p_filesz, get_file_offset(phdr[i].p_paddr), offset);

		p = p + get_file_offset(phdr[i].p_paddr);
		//lseek(phy_fd, get_file_offset(phdr[i].p_paddr), SEEK_SET);
#if 0
		offset = lseek( phy_fd, 0, SEEK_CUR );
		printf(" before read :%x \n",offset);
#endif
		unsigned long len = phdr[i].p_memsz;
		while (len > 0) {
			int tlen = PAGE_SIZE;
			if (len < PAGE_SIZE)
				tlen = len;
			//read(phy_fd, temp_buf, tlen + 8);

			write(fd, p, tlen);
			p=p+tlen +8;
			len = len - tlen;
		}
	}
	close(fd);

	return 1;
}
#if 0 /* Jiny adress space using the fixed address without pagetables
unsigned long start_address = 0x40000000;
int generate_program_section(unsigned long start, unsigned long end,
		int compr_type) {
	int i = total_phdrs;

	phdr[i].p_paddr = start;
	phdr[i].p_vaddr = phdr[i].p_paddr + start_address;
	phdr[i].p_filesz = end - start + 0x1000;
	phdr[i].p_memsz = phdr[i].p_filesz;
	phdr[i].p_type = PT_LOAD;
	phdr[i].p_flags = PF_R | PF_X;
	phdr[i].p_offset = file_offset;
	if (compr_type == NON_COMPRESSEED) {
		file_offset = file_offset + phdr[i].p_filesz;
	} else {
		phdr[i].p_offset = 0;
		if (phdr[i].p_filesz > max_zeropages) {
			max_zeropages = phdr[i].p_filesz;
			zerppage_index = i;
		}
	}
	total_phdrs++;

	return 1;
}
void mem_analysis() {
	int i;
	int continous_compressed = 0;

	unsigned long start, end, diff;
	start = 0;
	end = 0;
	for (i = 0; i < total_pages; i++) {
		if (phymem_offset[i].compress != NON_COMPRESSEED) { /* compressed */
			if (end > start) {

				start = start * 0x1000 + start_address + 0x1000;
				end = end * 0x1000 + start_address;
				diff = end - start + 0x1000;
				generate_program_section(start - start_address,
						end - start_address, NON_COMPRESSEED);

				printf(" %x - %x  : %dk (%xk) %dM\n", start, end, diff / 1024,
						diff / 1024, diff / (1024 * 1024));
			}
			start = i + 1;
			continous_compressed++;
		} else { /* if addr is not compressed */
			if (continous_compressed > 0) {
				unsigned long s, e;

				e = end * 0x1000 + start_address;
				s = e - (continous_compressed * 0x1000) + 0x1000;
				diff = e - s + 0x1000;
				continous_compressed = 0;
				generate_program_section(s - start_address, e - start_address,
						0);
				printf("Compressed:  %x - %x  : %dk (%xk) %dM\n", s, e,
						diff / 1024, diff / 1024, diff / (1024 * 1024));
			}
		}
		end = i + 1;
	}

	return;
}
#endif

#if 0 /* defined in elf.h */
typedef struct {
  Elf64_Word n_namesz; /* Length of the note's name. */
  Elf64_Word n_descsz; /* Length of the note's descriptor. */
  Elf64_Word n_type; /* Type of the note. */
} Elf64_Nhdr;
#endif
typedef struct elf_timeval {    /* Time value with microsecond resolution    */
  long tv_sec;                  /* Seconds                                   */
  long tv_usec;                 /* Microseconds                              */
} elf_timeval;
typedef struct elf_siginfo {    /* Information about signal (unused)         */
  int32_t si_signo;             /* Signal number                             */
  int32_t si_code;              /* Extra code                                */
  int32_t si_errno;             /* Errno                                     */
} elf_siginfo;

typedef struct x86_64_regs {    /* Normal (non-FPU) CPU registers            */

  #define BP rbp
  #define SP rsp
  #define IP rip
  uint64_t  r15,r14,r13,r12,rbp,rbx,r11,r10;
  uint64_t  r9,r8,rax,rcx,rdx,rsi,rdi,orig_rax;
  uint64_t  rip,cs,eflags;
  uint64_t  rsp,ss;
  uint64_t  fs_base, gs_base;
  uint64_t  ds,es,fs,gs;

} x86_64_regs;

typedef struct prstatus {       /* Information about thread; includes CPU reg*/
  elf_siginfo    info;       /* Info associated with signal               */
  uint16_t       cursig;     /* Current signal                            */
  unsigned long  sigpend;    /* Set of pending signals                    */
  unsigned long  sighold;    /* Set of held signals                       */
  pid_t          pid;        /* Process ID                                */
  pid_t          ppid;       /* Parent's process ID                       */
  pid_t          pgrp;       /* Group ID                                  */
  pid_t          sid;        /* Session ID                                */
  elf_timeval    utime;      /* User time                                 */
  elf_timeval    stime;      /* System time                               */
  elf_timeval    cutime;     /* Cumulative user time                      */
  elf_timeval    cstime;     /* Cumulative system time                    */
  x86_64_regs      reg;        /* CPU registers                             */
  uint32_t       fpvalid;    /* True if math co-processor being used      */
} prstatus;
int get_note_size(){
	return sizeof(Elf64_Nhdr)+8+sizeof(prstatus) ;
}
prstatus prs;
int write_regs(unsigned long *regs) {
	memset(&prs,0,sizeof(prstatus));
	prs.reg.rax = regs[0];
	prs.reg.rcx = regs[1];
	prs.reg.rdx = regs[2];
	prs.reg.rbx = regs[3];
	prs.reg.rsp = regs[4];
	prs.reg.rbp = regs[5];
	prs.reg.rsi = regs[6];
	prs.reg.rdi = regs[7];
	/* TODO : need to fill other registers */
	printf("RSP RBP %x :%x \n",regs[4],regs[5]);
}
int write_note(int fd){

	Elf64_Nhdr  nhdr;
	char name[10];

	nhdr.n_namesz =5;
	nhdr.n_descsz = sizeof(prs);
	nhdr.n_type = NT_PRSTATUS;

	strcpy(name,"CORE");
	write(fd,&nhdr,sizeof(nhdr));
	write(fd,"CORE\0\0\0\0",8);
	write(fd,&prs,sizeof(prs));
	return sizeof(nhdr)+8+sizeof(prs) ;
}
