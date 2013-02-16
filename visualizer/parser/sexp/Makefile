sources = lex.yy.cpp $(wildcard *.cpp)
objects = $(sources:%.cpp=%.o)
libclient_objects = $(sources:%.cpp=libclient_%.o)

CFLAGS = -g -fPIC
CXXFLAGS= -g -fPIC

ifeq ($(TARGET),mingw)
CXX:=i586-mingw32-g++
CC:=i586-mingw32-gcc
AR:=i586-mingw32-ar
RANLIB:=i586-mingw32-ranlib
else
AR:=ar
RANLIB:=ranlib
endif

all: sexp.a libclient_sexp.a

clean:
	rm -f $(objects) $(libclient_objects) $(deps) sexp.a libclient_sexp.a

lex.yy.h:
lex.yy.cpp: sexp.l
	 flex --outfile=lex.yy.cpp --header-file=lex.yy.h sexp.l

%.o: %.cpp
	$(CC) $(CFLAGS) $(CPPFLAGS) -c -o $@ $<

libclient_%.o: override CFLAGS += -fPIC
libclient_%.o: %.cpp
	$(CC) $(CFLAGS) $(CPPFLAGS) -c -o $@ $<

.PHONY: clean all

libclient_sexp.a: ${libclient_objects}
	$(AR) cr $@ $^
	$(RANLIB) $@

sexp.a: ${objects}
	$(AR) cr $@ $^
	$(RANLIB) $@

