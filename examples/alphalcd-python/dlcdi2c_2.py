class LcdI2c(object):
    def __init__(self):
        self.dev_filename = '/dev/lcdi2c'
        self.dev_meta_filename = '/sys/class/alphalcd/lcdi2c/meta'

        f = os.open(self.dev_meta_filename, os.O_RDONLY)
        if f:
            meta = os.read(f, 512).decode('ascii').rstrip().split("\n")
            os.close(f)
            self.columns, self.rows = [int(meta[v].split(":")[1]) for v in range(2,0,-1)]
            self.bufferlength = self.columns * self.rows
            try:
                iioc = meta.index("IOCTLS:") + 1
            except ValueError as e:
                print("No IOCTLS section in meta file")
                raise e
            self.ioctls = dict(k.split("=") for k in [s.lstrip() for s in meta[iioc:]])
        else:
            print("Unable to open meta file for driver")



    def write(self, input: str):
        output = bytes(input, encoding='ascii')
        f = open(self.dev_filename, 'rb+')
        f.write(output)
        f.close()