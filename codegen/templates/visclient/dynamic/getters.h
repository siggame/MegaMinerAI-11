#ifndef GETTERS_H 
#define GETTERS_H
#include "vc_structures.h"

#ifdef _WIN32
#define DLLEXPORT extern "C" __declspec(dllexport)
#else
#define DLLEXPORT
#endif

namespace client
{

#ifdef __cplusplus
extern "C" {
#endif

% for model in models:
%   for datum in model.data:
DLLEXPORT ${conversions[datum.type]} ${lowercase(model.name)}Get${capitalize(datum.name)}(_${model.name}* ptr);
%   endfor

%   for property in model.properties:
DLLEXPORT ${conversions[property.result]} ${lowercase(model.name)}Get${capitalize(property.name)}(_${model.name}* ptr\
%     for arg in property.arguments:
, \
${conversions[arg.type]} ${arg.name}\
%     endfor
);
%   endfor

% endfor

#ifdef __cplusplus
}
#endif

}

#endif
