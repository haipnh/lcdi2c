import os

bus=1
address=0x27

f = open("/sys/bus/i2c/devices/{0}-{1:04x}/name".format(bus, address))
name = "/dev/{0}".format(f.read().strip())
f.close()
print(name)

f = os.open("/sys/class/alphalcd/lcdi2c/meta", os.O_RDONLY)
if f:
    meta = os.read(f, 512).decode('utf8').rstrip().split("\n")
    print(meta)
    os.close(f)
    columns, rows = [int(meta[v].split(":")[1]) for v in range(2,0,-1)]
    bufferlength = columns * rows
    print(bufferlength)

    iioc = meta.index("IOCTLS:") + 1
    print(iioc)
    ioctls = dict(k.split("=") for k in [s.lstrip() for s in meta[iioc:]])
    print(ioctls)

