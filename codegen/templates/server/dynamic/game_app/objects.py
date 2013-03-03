% for model in models:
class ${model.name}\
%   if model.parent:
(${model.parent.name})\
%   else:
(object)\
%   endif
:
  game_state_attributes = ${[i.name for i in model.data]}
  def __init__(self, game\
%   for datum in model.data:
, ${datum.name}\
%   endfor
):
    self.game = game
%   for datum in model.data:
    self.${datum.name} = ${datum.name}
%   endfor
    self.updatedAt = game.turnNumber

  def toList(self):
    return [\
%   for datum in model.data:
self.${datum.name}, \
%   endfor
]
  
  # This will not work if the object has variables other than primitives
  def toJson(self):
    return dict(\
%   for datum in model.data:
${datum.name} = self.${datum.name}, \
%   endfor
)
  
  def nextTurn(self):
    pass

%   for func in model.functions:
  def ${func.name}(self\
%     for arg in func.arguments:
, ${arg.name}\
%     endfor
):
    pass

%   endfor
%   for prop in model.properties:
  def ${prop.name}(self\
%     for arg in prop.arguments:
, ${arg.name}\
%     endfor
):
    pass

%   endfor
  def __setattr__(self, name, value):
      if name in self.game_state_attributes:
        object.__setattr__(self, 'updatedAt', self.game.turnNumber)
      object.__setattr__(self, name, value)

% endfor

# The following are animations and do not need to have any logic added
% for animation in animations:
class ${animation.name[0].upper() + animation.name[1:]}Animation:
  def __init__(self\
%   for datum in animation.data:
, ${datum.name}\
%   endfor
):
%   for datum in animation.data:
    self.${datum.name} = ${datum.name}
%   endfor

  def toList(self):
    return ["${animation.name}", \
%   for datum in animation.data:
self.${datum.name}, \
%   endfor
]

  def toJson(self):
    return dict(type = "${animation.name}"\
%   for datum in animation.data:
, ${datum.name} = self.${datum.name}\
%   endfor
)

% endfor
