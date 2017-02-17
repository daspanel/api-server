# Determine this makefile's path.
# Be sure to place this BEFORE `include` directives, if any.
THIS_FILE := $(lastword $(MAKEFILE_LIST))

# Customize your project settings in this file.  
include ./make-project-settings.mk

PROJ=api_server
PGPIDENT="admindaspanel"
PYTHON=python
PYTEST=py.test
GIT=git
TOX=tox
NOSETESTS=nosetests
ICONV=iconv
FLAKE8=flake8
FLAKEPLUS=flakeplus
SPHINX2RST=sphinx2rst

TESTDIR=t
SPHINX_DIR=docs/
SPHINX_BUILDDIR="${SPHINX_DIR}/_build"
README=README.rst
README_SRC="docs/templates/readme.txt"
CONTRIBUTING=CONTRIBUTING.rst
CONTRIBUTING_SRC="docs/contributing.rst"
SPHINX_HTMLDIR="${SPHINX_BUILDDIR}/html"
DOCUMENTATION=Documentation
FLAKEPLUSTARGET=2.7

# Docker specific
# Based on https://github.com/UN-OCHA/docker-images
# The DockerHub repository name.
# This will also be used as the GITHUB_ORG tag in the image.
#ORGANISATION=daspanel
#IMAGE=api-server

# Initialise empty variables.
VERSION := latest
EXTRAVERSION := -dev

# Miscellaneous utilities used by the build scripts.
AWK=awk
DOCKER=docker
ECHO=echo
GREP=grep -E
MAKE=make
RM=rm
SED=sed
CP=cp
MKDIR=mkdir

all: help

help:
	@echo "docs                 - Build documentation."
	@echo "test-all             - Run tests for all supported python versions."
	@echo "distcheck ---------- - Check distribution for problems."
	@echo "  test               - Run unittests using current python."
	@echo "  lint ------------  - Check codebase for problems."
	@echo "    apicheck         - Check API reference coverage."
	@echo "    configcheck      - Check configuration reference coverage."
	@echo "    readmecheck      - Check README.rst encoding."
	@echo "    contribcheck     - Check CONTRIBUTING.rst encoding"
	@echo "    flakes --------  - Check code for syntax and style errors."
	@echo "      flakecheck     - Run flake8 on the source code."
	@echo "      flakepluscheck - Run flakeplus on the source code."
	@echo "readme               - Regenerate README.rst file."
	@echo "contrib              - Regenerate CONTRIBUTING.rst file"
	@echo "clean-dist --------- - Clean all distribution build artifacts."
	@echo "  clean-git-force    - Remove all uncomitted files."
	@echo "  clean ------------ - Non-destructive clean"
	@echo "    clean-pyc        - Remove .pyc/__pycache__ files"
	@echo "    clean-docs       - Remove documentation build artifacts."
	@echo "    clean-build      - Remove setup artifacts."
	@echo "docker-file -------- - Create default Dockerfile."
	@echo "docker ------------- - Create docker image."
	@echo "  docker-clean       - Clean docker build info."
	@echo "  docker-tag         - Tag last built docker image."
	@echo "docker-clean-images  - Clean all images from last buildlog.txt."

clean: clean-docs clean-pyc clean-build

clean-dist: clean clean-git-force

Documentation:
	(cd "$(SPHINX_DIR)"; $(MAKE) html)
	mv "$(SPHINX_HTMLDIR)" $(DOCUMENTATION)

docs: Documentation

clean-docs:
	-rm -rf "$(SPHINX_BUILDDIR)"

lint: flakecheck apicheck configcheck readmecheck

apicheck:
	(cd "$(SPHINX_DIR)"; $(MAKE) apicheck)

configcheck:
	(cd "$(SPHINX_DIR)"; $(MAKE) configcheck)

flakecheck:
	$(FLAKE8) --ignore=X999 "$(PROJ)" "$(TESTDIR)"

flakediag:
	-$(MAKE) flakecheck

flakepluscheck:
	$(FLAKEPLUS) --$(FLAKEPLUSTARGET) "$(PROJ)" "$(TESTDIR)"

flakeplusdiag:
	-$(MAKE) flakepluscheck

flakes: flakediag flakeplusdiag

clean-readme:
	-rm -f $(README)

readmecheck:
	$(ICONV) -f ascii -t ascii $(README) >/dev/null

$(README):
	$(SPHINX2RST) "$(README_SRC)" --ascii > $@

readme: clean-readme $(README) readmecheck

clean-contrib:
	-rm -f "$(CONTRIBUTING)"

$(CONTRIBUTING):
	$(SPHINX2RST) "$(CONTRIBUTING_SRC)" > $@

contrib: clean-contrib $(CONTRIBUTING)

clean-pyc:
	-find . -type f -a \( -name "*.pyc" -o -name "*$$py.class" \) -exec rm -f {} +
	-find . -type f -a \( -name "*.pyo" -o -name "*~" \) -exec rm -f {} +
	-find . -type d -name '__pycache__' -exec rm -fr {} +

removepyc: clean-pyc

clean-build:
	rm -rf build/ dist/ .eggs/ *.egg-info/ .tox/ .coverage cover/

clean-git:
	echo "*** NOT IMPLEMENTED ***"
	#$(GIT) clean -xdn

clean-git-force:
	echo "*** NOT IMPLEMENTED ***"
	#$(GIT) clean -xdf

test-all: clean-pyc
	$(TOX)

test:
	$(PYTHON) setup.py test

cov:
	$(PYTEST) -x --cov="$(PROJ)" --cov-report=html)

build:
	$(PYTHON) setup.py sdist bdist_wheel

distcheck: lint test clean

dist: readme contrib clean-dist build

# DOCKER specific
# Common build targets.
#docker: docker-clean docker-template
docker: clean-pyc docker-clean
	$(DOCKER) build \
		--build-arg VCS_REF=`git rev-parse --short HEAD` \
		--build-arg VCS_URL=`git config --get remote.origin.url | sed 's#git@github.com:#https://github.com/#'` \
		--build-arg BUILD_DATE=`date -u +"%Y-%m-%dT%H:%M:%SZ"` \
		--build-arg VERSION=$(VERSION) \
		. | tee buildlog.txt
	@$(MAKE) -f $(THIS_FILE) docker-tag # invoke other target

# Create a Dockerfile from the template.
docker-file:
	@$(ECHO) "Generating a Dockerfile for version $(VERSION)"
	@$(SED) "s/%%VERSION%%/$(VERSION)/" < Docker/default/Dockerfile.tmpl > Dockerfile

# Tag the image with our organisation, name and version.
docker-tag:
	@$(ECHO) "Tagging the built image."
	$(eval IMAGE_HASH=$(shell tail -n 1 buildlog.txt | $(AWK) '{print $$NF}'))
	$(DOCKER) tag $(IMAGE_HASH) $(GITHUB_ORG)/$(IMAGE):$(VERSION)$(EXTRAVERSION)

# Remove the buildlog.
docker-clean:
	$(RM) -f buildlog.txt

# Push the tagged image to DockerHub.
docker-push:
	$(DOCKER) push $(GITHUB_ORG)/$(IMAGE):$(VERSION)$(EXTRAVERSION)

# Remove intermediate images.
docker-clean-images:
	@echo Clean up intemediate images.
	for i in `$(GREP) '^ ---> ([a-z0-9]){12}$$' buildlog.txt | $(AWK) '{print $$2}'`; do \
		$(DOCKER) rmi -f $$i; \
	done

