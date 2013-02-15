INCLUDEPATH +=  ../interfaces \
                ../common/ \
                ./parser/

DEPENDPATH += ../common/ 

TEMPLATE = lib
TARGET = ${lowercase(gameName)}
SOURCES = *.cpp \
          ./parser/*.cpp \
          ./parser/sexp/*.cpp \
          ../common/*.cpp

HEADERS +=  *.h \
            ./parser/*.h \
            ./parser/sexp/*.h

CONFIG += config plugin dll 
debug:DEFINES += __DEBUG__
#QMAKE_CFLAGS_DEBUG += -pg
#QMAKE_CXXFLAGS_DEBUG += -pg
QMAKE_LFLAGS_DEBUG += -shared -Wl
QMAKE_LFLAGS_RELEASE += -shared -Wl
DEFINES += YY_NO_UNISTD_H PERFT_FAST
DESTDIR = ../plugins/

QMAKE_CXXFLAGS += -std=c++0x
QMAKE_CXXFLAGS_DEBUG += -std=c++0x

QT += opengl
