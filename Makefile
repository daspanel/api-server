
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
