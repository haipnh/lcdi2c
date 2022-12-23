TOOLS := /usr/bin
PREFIX := aarch64-linux-gnu-
KDIR := /mnt/nfs_server/linux/5.15.84
PWD := $(shell pwd)

obj-m :=  lcdi2c.o

all:
	$(MAKE) -C $(KDIR) \
		M=$(PWD) \
		ARCH=arm64 CROSS_COMPILE=$(TOOLS)/$(PREFIX) \
		modules

clean:
	$(MAKE) -C $(KDIR) M=$(PWD) clean

