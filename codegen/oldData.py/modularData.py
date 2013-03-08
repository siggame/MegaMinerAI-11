# -*- coding: iso-8859-1 -*-
from structures import *

aspects = []

Mappable = Model('Mappable', 
  data = [ Variable('x', int, 'The X position of the top left corner of this object.  X is horizontal'),
    Variable('y', int, 'The Y position of the top left corner of this object.  Y is vertical'),
    ],
  doc = 'An object that exists on the grid',
  type = 'virtual'
  )

Unit = Model('Unit', 
  parent = Mappable,
  data = [ Variable('owner', int, 'The owning player'),
    Variable('health', int, 'How much health this unit currently has'),
    Variable('maxHealth', int, 'The maximum amount of health this unit can ever have'),
    Variable('size', int, 'The length of one side of this Unit'),
    ],
  functions = [
    Function('talk',
      arguments = [ Variable('message', str,'The message this unit should say'),],
      doc = 'Sends a message to be visualized when this unit is selected'
      ),],
  doc = 'An object that exists on the grid',
  type = 'virtual'
  )

type = Model('Type',
  data = [Variable('name', str, 'The name of this type of robot'),
    Variable('maxHealth', int, 'The maximum amount of health for this type of robot'),
    Variable('damage', int, 'The amount of damage this type of robot does when attacking'),
    Variable('range', int, 'How far this type of robot can attack or heal from its edge'),
    Variable('movitude', int, 'This value divided by the number of bots = maxSteps for this type of robot'),
    Variable('actitude', int, 'This value divided by the number of bots = maxActions for this type of robot'),
    Variable('buildRate', int, 'This value is used to determine how many turns it takes to build a robot and how much this type of robot heals for'),
    ],
  doc = 'A kind of robot.'
  )

Wall = Model('Wall',
  parent = Unit,
  doc = 'A pile of hard stuff that is in the way.')

Frame = Model('Frame',
  parent = Unit,
  data = [Variable('type', type, 'What type this robot will be'),
    Variable('completionTime', int, 'How many of your turns until this frame becomes a robot' )],
  doc = 'A baby robot.')


#Split up the Bot class because of self-referential variables

Bot = Model('Bot',
  parent = Unit,
  doc = 'The bot class.')

Bot.addData([
    Variable('actions', int, 'How many actions this bot can still perform'),
    Variable('steps', int, 'How many steps this bot can still take'),
    Variable('damage', int, 'The amount of damage this robot does when attacking'),
    Variable('range', int, 'How far this robot can attack or heal from its edge'),
    Variable('movitude', int, 'This value divided by the number of bots = maxSteps for this robot'),
    Variable('actitude', int, 'This value divided by the number of bots = maxActions for this robot'),
    Variable('buildRate', int,'This value is used to determine how many turns it takes to build a robot and how much this robot heals for'),
    Variable('partOf', int, 'ID of the robot this robot is apart of, 0 if not in a robot'),
    Variable('building', int, 'ID of the robot this robot is building, 0 if not building'),
    Variable('type', int, 'ID of the type this robot is, 0 if a combination')
  ])
    
Bot.addFunctions([
    Function('move',
      arguments = [Variable('direction', str),],
      result = bool,
      doc = 'Move in the indicated direction (U, D, L, or R).  U is y=y-1, L=x=x-1, such that the top left corner is (0,0). Requires the calling robot to have a step.'
      ),
    Function('attack',
      arguments = [Variable('target', Unit),],
      result = bool,
      doc = 'Attack the specified unit.  Requires the calling robot to have an action and for the target to be in range'
      ),
    Function('heal',
      arguments = [Variable('target', Bot),],
      result = bool,
      doc = 'Heals the indicated bot.  Requires the calling robot to have an action and for the target to be in range.  Heals for target.maxHealth * self.buildRate / (4 * target.size^2)'
      ),
    Function('build',
      arguments = [Variable('type', type), Variable('x', int), Variable('y', int), Variable('size', int), ],
      result = bool,
      doc = 'Begins building a new robot.  While building, the new robot will be a frame.  Requires the calling robot to have an action. X and Y must cause the new robot to be adjacent.  Size must be less than or equal to the calling robots size.  Completes in 8 * size^2 / self.buildRate turns'
      ),
    Function('combine',
      arguments = [Variable('bot2', Bot), Variable('bot3', Bot), Variable('bot4', Bot)],
      result = bool,
      doc = 'Combines four robots into one.  Requires all robots to have an action, be of the same size, and be arranged in a square'
    ),
    Function('split',
      arguments = [],
      result = bool,
      doc = 'Splits a compound bot into the 4 robots that combined to make it.  Requires the calling robot to have an action.'
    ),
  ])


Bot.addProperties([
  Function('maxActions',
    result = int,
    doc = 'Returns the maximum number of actions this robot can take per turn.'
    ),
  Function('maxSteps',
    result = int,
    doc = 'Returns the maximum number of steps this robot can take per turn.'
    ),
  ])

move = Animation("Move",
  data = [Variable("robot", Bot),
    Variable("direction", str)]
  )
add = Animation("Add",
  data = [Variable("robot", Unit)]
  )
remove = Animation("Remove",
  data = [Variable("robot", Unit)]
  )
talk = Animation("Talk",
  data = [Variable("speaker", Unit), Variable("message", str)]
  )
split = Animation("Split",
  data = [Variable("robot", Bot)]
  )
combine = Animation("Combine",
  data = [Variable("bot1", Bot), Variable("bot2", Bot), Variable("bot3", Bot), Variable("bot4", Bot)]
  )
attack = Animation("Attack",
  data = [Variable("attacker", Bot), Variable("victim", Unit)]
  )
heal = Animation("Heal",
  data = [Variable("healer", Bot), Variable("victim", Unit)]
  )
build = Animation("Build",
  data = [Variable("builder", Bot), Variable("frame", Frame)]
  )
collide = Animation("Collide",
  data = [Variable("attacker", Bot), Variable("victim", Unit), Variable("direction", str)]
  )





globals = [
  Variable('turnNumber', int, 'How many turns it has been since the beginning of the game'),
  Variable('playerID', int, 'Player Number; either 0 or 1'),
  Variable('boardX', int, 'Maximum valid position in the X (right) direction.  (0,0) is top left'),
  Variable('boardY', int, 'Maximum valid position in the Y (down) direction.  (0,0) is top left'),
  Variable('gameNumber', int, 'What number game this is for the server')
  ]

constants = [
  Variable('player0Name', str, 'Player 0\'s name'),
  Variable('player1Name', str, 'Player 1\'s name'),
  ]

import timerAspect
timerAspect.install()
