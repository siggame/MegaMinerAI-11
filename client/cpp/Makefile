sources = $(wildcard *.cpp)
headers = $(wildcard *.h)
objects = $(sources:%.cpp=%.o)
dependency = Makefile.dependencies
CFLAGS += -g -I../library
CXXFLAGS += -g -I../library

all: client

submit: client
	@echo "$(shell cd ..;sh submit.sh cpp)"

.PHONY: clean all subdirs

clean:
	rm -f $(objects) client $(dependency)
	make -C ../library clean

client: $(objects) ../library/client.a ../library/sexp/sexp.a
	$(CXX) $(LDFLAGS) $(LOADLIBES) $(LDLIBS) $^ -g -o client

../library/client.a:
	$(MAKE) -C $(dir $@) $(notdir $@)

../library/sexp/sexp.a:
	$(MAKE) -C $(dir $@) $(notdir $@)

$(dependency): $(sources) $(headers)
	$(CXX) -MM $(sources) $(CXXFLAGS) > $@

-include $(dependency)
