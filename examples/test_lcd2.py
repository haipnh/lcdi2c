""" IOCTLS
'GETCHAR': '0x8008F506',
'SETCHAR': '0x4008F506',
'GETPOSITION': '0x8008F50D',
'SETPOSITION': '0x4008F511',
'RESET': '0x4008F516',
'HOME': '0x4008F51A',
'GETBACKLIGHT': '0x8008F51E',
'SETBACKLIGHT': '0x4008F51E',
'GETCURSOR': '0x8008F522',
'SETCURSOR': '0x4008F522',
'GETBLINK': '0x8008F526',
'SETBLINK': '0x4008F526',
'SCROLLHZ': '0x4008F52A',
'GETCUSTOMCHAR': '0x8008F52D',
'SETCUSTOMCHAR': '0x4008F52D',
'CLEAR': '0x4008F532'
"""

import os, fcntl, array

dev_filename = '/dev/lcdi2c'
dev_meta_filename = '/sys/class/alphalcd/lcdi2c/meta'

ioctls = dict()
f = os.open(dev_meta_filename, os.O_RDONLY)
if f:
  meta = os.read(f, 512).decode('ascii').rstrip().split("\n")
  os.close(f)
  columns, rows = [int(meta[v].split(":")[1]) for v in range(2,0,-1)]
  bufferlength = columns * rows
  try:
    iioc = meta.index("IOCTLS:") + 1
  except ValueError as e:
    print("No IOCTLS section in meta file")
    raise e
  ioctls = dict(k.split("=") for k in [s.lstrip() for s in meta[iioc:]])
else:
    print("Unable to open meta file for driver")

f = open(dev_filename, 'rb+')

def write_ioctl(cmd: str, value):
    s = ''
    if isinstance(value, str):
        s = bytes(s, encoding='ascii')
    if isinstance(value, list):
        s = array.array('B')
        s.extend(value)
    # f = open(dev_filename, 'rb+')
    fcntl.ioctl(f, int(cmd, base=16), s)
    # f.close()

def write(input: str):
    output = bytes(input, encoding='ascii')
    # f = open(dev_filename, 'rb+')
    f.write(output)
    # f.close()

print(ioctls.keys())
"""
dict_keys(['GETCHAR', 'SETCHAR', 'GETPOSITION', 'SETPOSITION', 'RESET', 
'HOME', 'GETBACKLIGHT', 'SETBACKLIGHT', 'GETCURSOR', 'SETCURSOR', 'GETBLINK', 
'SETBLINK', 'SCROLLHZ', 'GETCUSTOMCHAR', 'SETCUSTOMCHAR', 'CLEAR'])
"""





"""
cmd = '0x4008f51e' # SETBACKLIGHT
s = '1' # ON
fcntl.ioctl(f, int(cmd, base=16), s)

s = array.array('B')
value = [49]
s.extend(value)
fcntl.ioctl(f, int(cmd, base=16), s)

cmd = '0x4008F511' # SETPOSITION
s = array.array('B')
value = [8,0]
s.extend(value)
fcntl.ioctl(f, int(cmd, base=16), s)

f.write(b"123")

f.close()
"""