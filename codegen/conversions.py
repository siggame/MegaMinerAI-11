# -*- coding: iso-8859-1 -*-
import structures


c = {}
c['conversions'] = {int:'int', str:'char*', float:'float', bool:'int', chr:'char'}

cpp = {}
cpp['conversions'] = {int:'int', str:'string', float:'float', bool:'int', chr:'char'}

java = {}
java['conversions'] = {int:'int', str:'String', float:'float', bool:'int', chr:'char'}

csharp = {}
csharp['fromClient'] = {int:'int', str:'IntPtr', float:'float', bool:'int', chr:'char'}
csharp['toClient'] = {int:'int', str:'string', float:'float', bool:'int', chr:'char'}
csharp['types'] = {int:'int', str:'string', float:'float', bool:'int', chr:'char'}

python = {}
python['conversions'] = {int:'c_int', str:'c_char_p', float:'c_float', bool:'c_int', chr:'c_char'}

server = {}
server['conversions'] = {int:'int', str:'str', float:'float', bool:'int', chr:'char'}

def addModels(data):
  for i in data.values():
      if isinstance(i, structures.Model):
        c['conversions'][i] = '_' + i.name + '*'
        java['conversions'][i] = 'Pointer'
        csharp['fromClient'][i] = 'IntPtr'
        csharp['toClient'][i] = 'IntPtr'
        csharp['types'][i] = i.name
        python['conversions'][i] = 'c_void_p'
        server['conversions'][i] = 'int'
