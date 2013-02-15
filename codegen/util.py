# -*- coding: iso-8859-1 -*-
def capitalize(str):
  if not str:
    return str
  return str[0].upper() + str[1:]

def lowercase(str):
  if not str:
    return str
  return str[0].lower() + str[1:]

def dashify(str):
  if not str:
    return str
  result = str[0].lower()
  for i in str[1:]:
    if i == i.upper():
      result += '-'
    result += i.lower()
  return result

def depends(model):
  depends = set()
  for variable in model.data:
    if variable.type not in [int, str, float, bool, chr, None]:
      depends.add(variable.type)
  for func in model.functions + model.properties:
    if func.result not in [int, str, float, bool, chr, None]:
      depends.add(func.result)
    for variable in func.arguments:
      if variable.type not in [int, str, float, bool, chr, None]:
        depends.add(variable.type)
  return depends
