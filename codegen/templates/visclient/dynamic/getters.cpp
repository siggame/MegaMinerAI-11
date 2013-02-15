#include "getters.h"

namespace client
{

% for model in models:
%   for datum in model.data:
DLLEXPORT ${conversions[datum.type]} ${lowercase(model.name)}Get${capitalize(datum.name)}(_${model.name}* ptr)
{
  return ptr->${datum.name};
}
%   endfor
%   for property in model.properties:
DLLEXPORT ${conversions[property.result]} ${lowercase(model.name)}Get${capitalize(property.name)}(_${model.name}* ptr\
%     for arg in property.arguments:
, \
${conversions[arg.type]} ${arg.name}\
%     endfor
)
{
  
}
%   endfor
% endfor

}
