JAVAFILES=$(shell ls *.java 2> /dev/null)

all: libclient.so Main.class

submit: Main.class
	@echo "$(shell cd ..;sh submit.sh c)"


libclient.so: ../library/*.cpp ../library/*.h
	$(MAKE) -C ../library/ libclient.so
	cp -f ../library/libclient.so libclient.so

Main.class: $(JAVAFILES) libclient.so
	javac -cp jna.jar:. $(JAVAFILES)

clean:
	rm -f *.class
	rm -f libclient.so
	make -C ../library clean
