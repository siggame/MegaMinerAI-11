all: libclient.so

submit: libclient.so
	@echo "$(shell cd ..;sh submit.sh c)"


libclient.so: ../library/*.cpp ../library/*.h
	$(MAKE) -C ../library/ libclient.so
	cp ../library/libclient.so libclient.so


clean:
	rm -f libclient.so
	rm -f *.pyc
	make -C ../library clean
