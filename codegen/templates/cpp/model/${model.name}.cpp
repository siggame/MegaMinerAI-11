// -*-c++-*-

#include "${model.name}.h"
#include "game.h"

% for dependency in depends(model):
#include "${dependency.name}.h"
% endfor

${model.name}::${model.name}(_${model.name}* pointer)
{
    ptr = (void*) pointer;
}

%   for datum in model.data:
${conversions[datum.type]} ${model.name}::${datum.name}()
{
  return ((_${model.name}*)ptr)->${datum.name};
}

%   endfor

%   for func in model.functions:
bool ${model.name}::${func.name}(\
%     for arg in func.arguments:
%       if func.arguments[0] != arg:
, \
%       endif
%       if isinstance(arg.type, Model):
${arg.type.name}& ${arg.name}\
%       else:
${conversions[arg.type]} ${arg.name}\
%       endif
%     endfor
)
{
  return ${lowercase(model.name)}${capitalize(func.name)}( (_${model.name}*)ptr\
%     for arg in func.arguments:
%       if isinstance(arg.type, Model):
, (_${arg.type.name}*) ${arg.name}.ptr\
%       else:
, ${arg.name}\
%       endif
%     endfor
);
}

%   endfor

%   for prop in model.properties:
${conversions[prop.result]} ${model.name}::${prop.name}(\
%     for arg in prop.arguments:
%       if prop.arguments[0] != arg:
, \
%       endif
%       if isinstance(arg.type, Model):
${arg.type.name}& ${arg.name}\
%       else:
${conversions[arg.type]} ${arg.name}\
%       endif
%     endfor
)
{
  return ${lowercase(model.name)}${capitalize(prop.name)}( (_${model.name}*)ptr\
%     for arg in prop.arguments:
%       if isinstance(arg.type, Model):
, (_${arg.type.name}*) ${arg.name}.ptr\
%       else:
, ${arg.name}\
%       endif
%     endfor
);
}

%   endfor

std::ostream& operator<<(std::ostream& stream,${model.name} ob)
{
%   for datum in model.data:
  stream << "${datum.name}: " << ((_${model.name}*)ob.ptr)->${datum.name}  <<'\n';
%   endfor
  return stream;
}
