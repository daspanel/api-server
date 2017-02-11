include ../../Makefile-Docker.conf
include ../Makefile.conf

VERSION=$$(VERSION)
#UPSTREAM=$$(UPSTREAM))

all: build tag

mrproper: clean_images clean

# Put source code
source: clean-source
	$(CP) -dpR ../../container_data/* rootfs/.
	$(MKDIR) -p rootfs/opt/daspanel/apiserver
	$(CP) -dpR ../../api_server rootfs/opt/daspanel/apiserver/.

# Cleans sources
clean-source:
	$(RM) -Rf rootfs/*

