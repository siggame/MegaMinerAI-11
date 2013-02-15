import com.sun.jna.Library;
import com.sun.jna.Pointer;
import com.sun.jna.Native;

public interface Client extends Library {
  Client INSTANCE = (Client)Native.loadLibrary("client", Client.class);
  Pointer createConnection();
  boolean serverConnect(Pointer connection, String host, String port);

  boolean serverLogin(Pointer connection, String username, String password);
  int createGame(Pointer connection);
  int joinGame(Pointer connection, int id, String playerType);

  void endTurn(Pointer connection);
  void getStatus(Pointer connection);

  int networkLoop(Pointer connection);


    //commands
% for  model in models:
%   for func in model.functions:
  int ${lowercase(model.name)}${capitalize(func.name)}(Pointer object\
%     for arg in func.arguments:
, \
${conversions[arg.type]} ${arg.name}\
%     endfor
);
%   endfor
% endfor

    //accessors
% for datum in globals:
  ${conversions[datum.type]} get${capitalize(datum.name)}(Pointer connection);
% endfor

% for model in models:
%   if model.type == 'Model':
  Pointer get${model.name}(Pointer connection, int num);
  int get${model.name}Count(Pointer connection);
%   endif
% endfor


    //getters
% for model in models:
%   for datum in model.data:
  ${conversions[datum.type]} ${lowercase(model.name)}Get${capitalize(datum.name)}(Pointer ptr);
%   endfor

% endfor

    //properties
% for  model in models:
%   for prop in model.properties:
  ${conversions[prop.result]} ${lowercase(model.name)}${capitalize(prop.name)}(Pointer object\
%     for arg in prop.arguments:
, \
${conversions[arg.type]} ${arg.name}\
%     endfor
);
%   endfor
% endfor

}
