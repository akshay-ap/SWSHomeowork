# Problem 1

# Helpful commands

gdb -q sof-exploit-reverse-target
list
break 9
run $(cat file.txt)
info registers
x/40x $esp

# Solution

gcc -fno-stack-protector -O0 -ggdb3 -o s1 sof-exploit-reverse-exploit.c
gcc -fno-stack-protector -O0 -ggdb3 -o sof-exploit-reverse-target sof-exploit-reverse-target.c
./s1 bffffdc8
