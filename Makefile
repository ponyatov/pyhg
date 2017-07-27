## versions 

JYTHON_VER = 2.7.0
PLY_VER = 3.10
HGDB_VER = 1.3

## packages

JYTHON = jython-standalone-2.7.0.jar
PLY = ply-$(PLY_VER)
HGDB = hypergraphdb-$(HGDB_VER)

PLY_GZ = $(PLY).tar.gz
HGDB_GZ = hgdbdist-$(HGDB_VER)-final.tar.gz

PKGS = lib/$(JYTHON) lib/$(PLY)/README.md lib/$(HGDB)/readme.html

HGDB_LIB = lib/$(HGDB)/lib/hgdb-$(HGDB_VER).jar:lib/$(HGDB)/lib/hgbdbje-$(HGDB_VER).jar:lib/$(HGDB)/lib/je-5.0.34.jar

## test run (make default)

test.log : test.src test.py lib/$(JYTHON) $(PKGS) Makefile
	JYTHONPATH=lib/$(PLY):$(HGDB_LIB) java -cp $(HGDB_LIB) -jar lib/$(JYTHON) test.py
	
## installation

WGET = wget -c -O $@

.PHONY: install 
install: $(PKGS)

lib/$(JYTHON):
	$(WGET) http://search.maven.org/remotecontent?filepath=org/python/jython-standalone/$(JYTHON_VER)/$(JYTHON)

lib/$(PLY_GZ):
	$(WGET) http://www.dabeaz.com/ply/$(PLY_GZ)
lib/$(PLY)/README.md: lib/$(PLY_GZ)
	cd lib ; tar zx < $(PLY_GZ)
	touch $@

lib/$(HGDB)/readme.html: lib/$(HGDB_GZ)
	cd lib ; tar zx < $(HGDB_GZ)
	touch $@
lib/$(HGDB_GZ):
	$(WGET) http://hypergraphdb.org/files/$(HGDB_GZ)
