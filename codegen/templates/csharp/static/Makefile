CSFILES=$(shell ls *.cs 2> /dev/null)

all: libclient.so client.exe

submit: Main.class
	@echo "$(shell cd ..;sh submit.sh c)"


libclient.so: ../library/*.cpp ../library/*.h
	$(MAKE) -C ../library/ libclient.so
	cp -f ../library/libclient.so libclient.so

client.exe: $(CSFILES) libclient.so
	gmcs -out:client.exe  $(CSFILES)

clean:
	rm -f client.exe
	rm -f libclient.so
	make -C ../library clean
