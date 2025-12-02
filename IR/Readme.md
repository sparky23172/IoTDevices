# IR projects

---

## irB0D3TK3HTX.py

Used for the light sticks.

### TLDR;

```
00000000 = None
11110111 = What device is listening for
11000000 = 3    # Command
00111111 = OR 3 # Checksum

Send over PWM 38000

0x0-0x17, 0x255 # Possible values that are tied to the remote
```

---

## nec.py

Captures signal and then shows the NEC values
``` python
print(binary[0:8])
print(binary[8:16])
print(binary[16:24])
print(binary[24:32])
print(binary)
```
Super useful for converting commands into irB0D3TK3HTX programs!

---
