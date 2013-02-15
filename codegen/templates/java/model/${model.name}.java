import com.sun.jna.Pointer;

///${model.doc}
% if model.type == 'virtual':
abstract \
% endif
class ${model.name}\
% if model.parent:
 extends ${model.parent.name}\
% endif

{
% if not model.parent:
  Pointer ptr;
  int ID;
  int iteration;
  public ${model.name}(Pointer p)
  {
    ptr = p;
    ID = Client.INSTANCE.${lowercase(model.name)}GetId(ptr);
    iteration = BaseAI.iteration;
  }
% else:
  public ${model.name}(Pointer p)
  {
    super(p);
  }
% endif
% if model.type == 'virtual':
  abstract boolean validify();
% else:
  boolean validify()
  {
    if(iteration == BaseAI.iteration) return true;
    for(int i = 0; i < BaseAI.${lowercase(model.plural)}.length; i++)
    {
      if(BaseAI.${lowercase(model.plural)}[i].ID == ID)
      {
        ptr = BaseAI.${lowercase(model.plural)}[i].ptr;
        iteration = BaseAI.iteration;
        return true;
      }
    }
    throw new ExistentialError();
  }
% endif

    //commands

% for func in model.functions:
  ///${func.doc}
  boolean ${func.name}(\
%   for arg in func.arguments:
%     if func.arguments[0] is not arg:
, \
%     endif
%     if isinstance(arg.type, Model):
${arg.type.name} ${arg.name}\
%     else:
${conversions[arg.type]} ${arg.name}\
%     endif
%   endfor
)
  {
    validify();
%   for arg in func.arguments:
%     if isinstance(arg.type, Model):
    ${arg.name}.validify();
%     endif
%   endfor
    return (Client.INSTANCE.${lowercase(model.name)}${capitalize(func.name)}(ptr\
%   for arg in func.arguments:
, \
%     if isinstance(arg.type, Model):
${arg.name}.ptr\
%     else:
${arg.name}\
%     endif
%   endfor
) == 0) ? false : true;
  }
% endfor

    //getters

% for datum in model.data:
  ///${datum.doc}
  public ${conversions[datum.type]} get${capitalize(datum.name)}()
  {
    validify();
    return Client.INSTANCE.${lowercase(model.name)}Get${capitalize(datum.name)}(ptr);
  }
% endfor

% for prop in model.properties:
   ///${prop.doc}
%     if isinstance(prop.type, Model):
  int \
%     else:
  ${conversions[prop.type]} \
%     endif
get${capitalize(prop.name)}(\
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
)
  {
    validify();
    return Client.INSTANCE.${lowercase(model.name)}${capitalize(prop.name)}(ptr\
%   for arg in prop.arguments:
%     if isinstance(arg.type, Model):
, (_${arg.type.name}*) ${arg.name}.ptr\
%     else:
, ${arg.name}\
%     endif
%   endfor
);
  }

%   endfor
}
