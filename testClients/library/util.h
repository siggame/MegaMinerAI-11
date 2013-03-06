#ifndef UTIL_H
#define UTIL_H

#ifdef _WIN32
#define DLLEXPORT extern "C" __declspec(dllexport)
#else
#define DLLEXPORT
#endif

#ifdef __cplusplus
extern "C"
{
#endif
  
#ifdef __cplusplus
}
#endif

#endif
