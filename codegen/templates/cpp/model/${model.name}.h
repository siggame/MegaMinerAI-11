// -*-c++-*-

#ifndef ${model.name.upper()}_H
#define ${model.name.upper()}_H

#include <iostream>
#include "structures.h"

% if model.parent:
#include "${model.parent.name}.h"
% endif
% for dependency in depends(model):
class ${dependency.name};
% endfor

% if model.doc:
///${model.doc}
% endif
class ${model.name} \
% if model.parent:
: public ${model.parent.name} \
% endif
{
  public:
% if not model.parent:
  void* ptr;
% endif
  ${model.name}(_${model.name}* ptr = NULL);

  // Accessors
% for datum in model.data:
  ///${datum.doc}
  ${conversions[datum.type]} ${datum.name}();
% endfor

  // Actions
% for func in model.functions:
  ///${func.doc}
  bool ${func.name}(\
%   for arg in func.arguments:
%     if func.arguments[0] != arg:
, \
%     endif
%     if isinstance(arg.type, Model):
${arg.type.name}& ${arg.name}\
%     else:
${conversions[arg.type]} ${arg.name}\
%     endif
%   endfor
);
% endfor

  // Properties
% for prop in model.properties:
  ///${prop.doc}
  ${conversions[prop.result]} ${prop.name}(\
%   for arg in prop.arguments:
%     if prop.arguments[0] != arg:
, \
%     endif
%     if isinstance(arg.type, Model):
${arg.type.name}& ${arg.name}\
%     else:
${conversions[arg.type]} ${arg.name}\
%     endif
%   endfor
);
% endfor


  friend std::ostream& operator<<(std::ostream& stream, ${model.name} ob);
};

#endif

