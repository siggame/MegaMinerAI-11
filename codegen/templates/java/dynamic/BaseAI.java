import com.sun.jna.Pointer;

/// \brief A basic AI interface.

///This class implements most the code an AI would need to interface with the lower-level game code.
///AIs should extend this class to get a lot of builer-plate code out of the way
///The provided AI class does just that.
public abstract class BaseAI
{
% for model in models:
%   if model.type == 'Model':
  static ${model.name}[] ${lowercase(model.plural)};
%   endif
% endfor
  Pointer connection;
  static int iteration;
  boolean initialized;

  public BaseAI(Pointer c)
  {
    connection = c;
  }
    
  ///
  ///Make this your username, which should be provided.
  public abstract String username();
  ///
  ///Make this your password, which should be provided.
  public abstract String password();
  ///
  ///This is run on turn 1 before run
  public abstract void init();
  ///
  ///This is run every turn . Return true to end the turn, return false
  ///to request a status update from the server and then immediately rerun this function with the
  ///latest game status.
  public abstract boolean run();

  ///
  ///This is run on after your last turn.
  public abstract void end();


  public boolean startTurn()
  {
    iteration++;
    int count = 0;
% for model in models:
%   if model.type == 'Model':
    count = Client.INSTANCE.get${model.name}Count(connection);
    ${lowercase(model.plural)} = new ${model.name}[count];
    for(int i = 0; i < count; i++)
    {
      ${lowercase(model.plural)}[i] = new ${model.name}(Client.INSTANCE.get${model.name}(connection, i));
    }
%   endif
% endfor

    if(!initialized)
    {
      initialized = true;
      init();
    }
    return run();
  }


% for datum in globals:
  ///${datum.doc}
  ${conversions[datum.type]} ${datum.name}()
  {
    return Client.INSTANCE.get${capitalize(datum.name)}(connection);
  }
% endfor
}
