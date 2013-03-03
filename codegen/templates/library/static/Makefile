sources = $(wildcard *.cpp)
headers = $(wildcard *.h)
objects = $(sources:%.cpp=%.o)
dependency = Makefile.dependencies
CFLAGS += -g
CXXFLAGS += -g

#Uncomment this line to get a boatload of debug output.
#CPPFLAGS = -DSHOW_NETWORK
#override CPPFLAGS += -DSHOW_WARNINGS

override CPPFLAGS += -Isexp

all: libclient.so client.a

submit: client
	@echo "$(shell cd ..;sh submit.sh c)"

.PHONY: clean all subdirs

libclient_%.o: override CXXFLAGS += -fPIC
libclient_%.o: %.cpp *$(headers)
	$(CXX) $(CXXFLAGS) $(CPPFLAGS) -c -o $@ $<

clean:
	rm -f $(objects) client client.a libclient_network.o libclient_game.o libclient_getters.o libclient_util.o libclient.so
	$(MAKE) -C sexp clean

libclient.so: libclient_network.o libclient_game.o libclient_getters.o libclient_util.o sexp/libclient_sexp.a
	$(CXX) -shared -Wl,-soname,libclient.so $(LDFLAGS) $(LOADLIBES) $(LDLIBS) $^ -o libclient.so
client.a: $(objects)
	ar cr $@ $^
	ranlib $@

sexp/sexp.a sexp/libclient_sexp.a:
	$(MAKE) -C $(dir $@) $(notdir $@)

$(dependency): $(sources) $(headers)
	$(CXX) -MM $(sources) $(CXXFLAGS) > $@

-include $(dependency)
