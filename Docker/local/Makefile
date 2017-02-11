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
	$(CP) -dpR ../../requirements rootfs/opt/daspanel/apiserver/.
	-find rootfs/. -type f -a \( -name "*.pyc" -o -name "*$$py.class" \) -exec rm -f {} +
	-find rootfs/. -type f -a \( -name "*.pyo" -o -name "*~" \) -exec rm -f {} +
	-find rootfs/. -type d -name '__pycache__' -exec rm -fr {} +

# Cleans sources
clean-source:
	$(RM) -Rf rootfs/*

