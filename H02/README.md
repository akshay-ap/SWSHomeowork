# Problem 1

gcc -fno-stack-protector -O0 -ggdb3 -o s1 sof-exploit-10-target.c

gdb -q s1
list
break 6
run $(cat e1)
info registers
x/80x $esp

https://samsclass.info/127/proj/p3-lbuf1.htm

esp 0xbffff600 0xbffff600
ebp 0xbffff708 0xbffff708

esp 0xbffff5c0 0xbffff5c0
ebp 0xbffff6c8 0xbffff6c8
