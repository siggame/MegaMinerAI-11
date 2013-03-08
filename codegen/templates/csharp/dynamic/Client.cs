using System;
using System.Runtime.InteropServices;

public class Client {
  [DllImport("client")]
  public static extern IntPtr createConnection();
  [DllImport("client")]
  public static extern int serverConnect(IntPtr connection, string host, string port);

  [DllImport("client")]
  public static extern int serverLogin(IntPtr connection, string username, string password);
  [DllImport("client")]
  public static extern int createGame(IntPtr connection);
  [DllImport("client")]
  public static extern int joinGame(IntPtr connection, int id, string playerType);

  [DllImport("client")]
  public static extern void endTurn(IntPtr connection);
  [DllImport("client")]
  public static extern void getStatus(IntPtr connection);

  [DllImport("client")]
  public static extern int networkLoop(IntPtr connection);


    //commands
% for  model in models:
%   for func in model.functions:
  [DllImport("client")]
  public static extern int ${lowercase(model.name)}${capitalize(func.name)}(IntPtr self\
%     for arg in func.arguments:
, \
${toClient[arg.type]} ${arg.name}\
%     endfor
);
%   endfor
% endfor

    //accessors
% for datum in globals:
  [DllImport("client")]
  public static extern ${fromClient[datum.type]} get${capitalize(datum.name)}(IntPtr connection);
% endfor

% for model in models:
%   if model.type == 'Model':
  [DllImport("client")]
  public static extern IntPtr get${model.name}(IntPtr connection, int num);
  [DllImport("client")]
  public static extern int get${model.name}Count(IntPtr connection);
%   endif
% endfor


    //getters
% for model in models:
%   for datum in model.data:
  [DllImport("client")]
  public static extern ${fromClient[datum.type]} ${lowercase(model.name)}Get${capitalize(datum.name)}(IntPtr ptr);
%   endfor

% endfor

    //properties
% for  model in models:
%   for prop in model.properties:
  [DllImport("client")]
  public static extern ${fromClient[prop.result]} ${lowercase(model.name)}${capitalize(prop.name)}(IntPtr self\
%     for arg in prop.arguments:
, \
${toClient[arg.type]} ${arg.name}\
%     endfor
);
%   endfor
% endfor

}
