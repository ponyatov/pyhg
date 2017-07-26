JYTHON_VER = 2.7.0
PLY_VER = 3.10

JYTHON = jython-standalone-2.7.0.jar
PLY = ply-$(PLY_VER)

PLY_GZ = $(PLY).tar.gz

WGET = wget -c -O $@

.PHONY: install 
install: lib/$(JYTHON) lib/$(PLY)/README.md

lib/$(JYTHON):
	$(WGET) http://search.maven.org/remotecontent?filepath=org/python/jython-standalone/$(JYTHON_VER)/$(JYTHON)

lib/$(PLY_GZ):
	$(WGET) http://www.dabeaz.com/ply/$(PLY_GZ)
lib/$(PLY)/README.md: lib/$(PLY_GZ)
	cd lib ; tar zx < $(PLY_GZ)
	touch $@