# -*- coding: iso-8859-1 -*-
from structures import *

aspects = ['timer']

gameName = "Space"

globals = [ Variable('turnNumber', int, 'How many turns it has been since
the beginning of the round'),
  Variable('playerID', int, 'Player Number; either 0 or 1'),
  Variable('gameNumber', int, 'What number game this is for the server'),
  Variable('roundNumber', int, 'The current round of the match'),
  Variable('victoriesNeeded', int, 'How many victories a player needs to win
  this game. If the last round is a tie, one more victory is needed'),
  Variable('mapRadius', int, 'The outer radius of the map. Center of screen
  is (0,0), with +x right, +y up'),
]

constants = [
  ]
  
playerData = [
  Variable('victories',int,'How many rounds you have won this game'),
  Variable('energy', int, 'How much energy the player has left to warp in
ships'),
  ]

playerFunctions = [
  Function('talk', [Variable('message', str)], doc='Allows a player to
display messages on the screen'),
  ]

ShipDescription = Model('ShipDescription',
  data=[
    Variable('type', str, 'The ship type'),
    Variable('cost', int, 'The amount of energy required to warp in this
type of ship'),
    Variable('radius', int, 'The radius of the ship'),
    Variable('range', int, 'The range of attacks for this ship, given as the
maximum distance from the center of this ship to the edge of the target'),
    Variable('damage', int, 'The strength of attacks for this ship'),
    Variable('selfDestructDamage', int, 'The amount of damage done when this
ship self destructs'),
    Variable('maxMovement', int, 'The largest possible movement for this
ship'),
Variable('maxAttacks', int, 'The max number of attacks for this ship'),
Variable('maxHealth', int, 'The max health possible for the ship'),
    ],
  doc='Base class for all variables needed to define a ship',
  type='virtual',
)

Ship = Model('Ship',
  parent=ShipDescription,
  data=[ Variable('owner', int, 'The owner of the ship'),
    Variable('x', int, 'X position of the ship'),
    Variable('y', int, 'Y position of the ship'),
Variable('attacksLeft', int, 'How many more attacks this ship can make this
turn'),
Variable('movementLeft', int, 'How much more this ship can move this turn'),
Variable('health', int, 'The current health of the ship'),
  ],

  functions=[
    Function('move', [Variable('x', int), Variable('y', int)], doc='Command
a ship to move to a specified position'),
    Function ('selfDestruct', [], doc='Blow yourself up, damage enemy ships
that overlap this ship'),
  ],
  doc="A space ship!",
)

Ship.addFunctions([Function("attack", [Variable("target", Ship)],
  doc='Commands your ship to attack a target.'
  )])

ShipType = Model('ShipType',
  parent=ShipDescription,
  functions=[Function('warpIn', [Variable('x', int), Variable('y', int)],
doc="Sends in a new ship of this type. Ships must be warped in within the
radius of the player's warp gate."),
    ],
  doc='An available ship type',
  )

move = Animation('move',
  data=[Variable('actingID', int),
    Variable('fromX', int),
    Variable('fromY', int),
    Variable('toX', int),
    Variable('toY', int),
    ],
  )

attack = Animation('attack',
  data=[
    Variable('actingID', int),
    Variable('targetID', int),
    ],
  )
  
selfDestruct = Animation ('selfDestruct' ,
  data=[
    Variable('actingID', int),
    ],
  )

stealth = Animation('stealth',
  data=[
    Variable('actingID', int),
    ],
  )
  
playerTalk = Animation('playerTalk',
  data=[
    Variable('actingID', int),
    Variable('message', str),
    ],
  )

deStealth = Animation('deStealth',
  data=[
    Variable('actingID', int),
    ],
  )
  
roundVictory = Animation('roundVictory',
  data=[
    Variable('identifier', int), #Magic number in the land of OZ: -17
    Variable('message', str),
  ],
)
