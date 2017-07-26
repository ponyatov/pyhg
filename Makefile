JYTHON_VER = 2.7.0

JYTHON = jython-standalone-2.7.0.jar

WGET = wget -c 
install: lib/$(JYTHON)

lib/$(JYTHON):
	$(WGET) -O $@ http://search.maven.org/remotecontent?filepath=org/python/jython-standalone/$(JYTHON_VER)/$(JYTHON)
