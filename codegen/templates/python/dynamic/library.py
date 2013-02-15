# -*-python-*-

import os

from ctypes import *

try:
  if os.name == 'posix':
    library = CDLL("./libclient.so")
  elif os.name == 'nt':
    library = CDLL("./client.dll")
  else:
    raise Exception("Unrecognized OS: "+os.name)
except OSError:
  raise Exception("It looks like you didn't build libclient. Run 'make' and try again.")

# commands

library.createConnection.restype = c_void_p
library.createConnection.argtypes = []

library.serverConnect.restype = c_int
library.serverConnect.argtypes = [c_void_p, c_char_p, c_char_p]

library.serverLogin.restype = c_int
library.serverLogin.argtypes = [c_void_p, c_char_p, c_char_p]

library.createGame.restype = c_int
library.createGame.argtypes = [c_void_p]

library.joinGame.restype = c_int
library.joinGame.argtypes = [c_void_p, c_int, c_char_p]

library.endTurn.restype = None
library.endTurn.argtypes = [c_void_p]

library.getStatus.restype = None
library.getStatus.argtypes = [c_void_p]

library.networkLoop.restype = c_int
library.networkLoop.argtypes = [c_void_p]

#Functions
%for model in models:
%  for func in model.functions:
library.${lowercase(model.name)}${capitalize(func.name)}.restype = c_int
library.${lowercase(model.name)}${capitalize(func.name)}.argtypes = [${conversions[model]}\
%    for arg in func.arguments:
, \
${conversions[arg.type]}\
%  endfor
]

% endfor
%endfor
# accessors

#Globals
%for datum in globals:
library.get${capitalize(datum.name)}.restype = ${conversions[datum.type]}
library.get${capitalize(datum.name)}.argtypes = [c_void_p]

%endfor
%for model in models:
%   if model.type == 'Model':
library.get${model.name}.restype = c_void_p
library.get${model.name}.argtypes = [c_void_p, c_int]

library.get${model.name}Count.restype = c_int
library.get${model.name}Count.argtypes = [c_void_p]

%   endif
%endfor
# getters

#Data
%for model in models:
%  for datum in model.data:
%    if not isinstance(datum.type, Model):
library.${lowercase(model.name)}Get${capitalize(datum.name)}.restype = ${conversions[datum.type]}
%    else:
library.${lowercase(model.name)}Get${capitalize(datum.name)}.restype = c_int
%    endif
library.${lowercase(model.name)}Get${capitalize(datum.name)}.argtypes = [c_void_p]

%  endfor
%endfor

#Properties
%for model in models:
%  for prop in model.properties:
library.${lowercase(model.name)}${capitalize(prop.name)}.restype = c_int
library.${lowercase(model.name)}${capitalize(prop.name)}.argtypes = [${conversions[model]}\
%    for arg in prop.arguments:
, \
${conversions[arg.type]}\
%  endfor
]

% endfor
%endfor
