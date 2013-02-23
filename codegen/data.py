# -*- coding: iso-8859-1 -*-
from structures import *

aspects = ['timer']

gameName = "Reef"

constants = [
  ]

playerData = [
  Variable('currentReefHealth', int, 'The player\'s current reef health'),
  Variable('spawnFood', int, 'Food used to spawn new fish'),
  ]

playerFunctions = [
  Function('talk', [Variable('message', str)], doc='Allows a player to display messages on the screen'),
]

Mappable = Model('Mappable',
  data=[
    Variable('x', int, 'X position of the object'),
    Variable('y', int, 'Y position of the object'),
  ],
  doc='A mappable object!',
)

globals = [
  Variable('initialFood', int, 'How much spawn food a player starts the game with'),
  Variable('sharedLowerBound', int, 'The lower x-value of the shared zone'),
  Variable('sharedUpperBound', int, 'The upper x-value of the shared zone'),
  Variable('spawnFoodPerTurn', int, 'How much spawn food a player receives each turn'),
  Variable('turnNumber', int, 'How many turns it has been since the beginning of the game'),
  Variable('playerID', int, 'Player Number; either 0 or 1'),
  Variable('gameNumber', int, 'What number game this is for the server'),
  Variable('turnsTillSpawn',int, 'Turns until you can spawn new fish'),
  Variable('maxReefHealth',int,'How much health a reef has initially'),
  Variable('trashDamage',int,'How much damage trash does'),
  Variable('mapWidth', int, 'How wide the map is'),
  Variable('mapHeight', int, 'How high the map is'),
  Variable('trashAmount',int, 'amount of trash in the game')
  ]

Tile = Model('Tile',
  parent = Mappable,
  data=[
    Variable('trashAmount', int, 'The amount of trash on this tile'),
    ],
  doc='Represents a single tile on the map, can contain some amount of trash. Example: 5 trash can be split to 2 and 3',
  )

FishSpecies = Model('FishSpecies',
  data = [
    Variable('species', str, 'The fish species'),
    Variable('cost', int, 'The amount of food it takes to raise this fish'),
    Variable('maxHealth', int, 'The maximum health of this fish'),
    Variable('maxMovement', int, 'The maximum number of movements in a turn'),
    Variable('carryCap', int, 'The total weight the fish can carry'),
    Variable('attackPower', int, 'The power of the fish\'s attack'),
    Variable('range',int,'The attack arrange of the fish'),
    Variable('maxAttacks',int,'Maximum number of times this unit can attack per turn'),
    Variable('canStealth', bool, 'If this species is able to use stealth'),
    Variable('turnsTillAvailalbe',int, 'How many turns until you can spawn this fish species'),
    Variable('turnsTillUnavailable', int, 'How many turns until you can no longer spawn this fish species'),
    ],
  functions=[
    Function('spawn',[Variable('x',int),Variable('y',int)],
    doc='Have a new fish spawn and join the fight!'),
    ],
  )
  
Fish = Model('Fish',
  parent=Mappable,
  data=[ Variable('owner', int, 'The owner of this fish'),
    Variable('maxHealth', int, 'The maximum health of the fish'),
    Variable('currentHealth', int, 'The current health of the fish'),
    Variable('maxMovement', int, 'The maximum number of movements in a turn'),
    Variable('movementLeft', int, 'The number of movements left'),
    Variable('carryCap', int, 'The total weight the fish can carry'),
    Variable('carryingWeight', int, 'The current amount of weight the fish is carrying'),
    Variable('attackPower', int, 'The power of the fish\'s attack'),
    Variable('isVisible', int, 'The visibleness of the fish'),
    Variable('maxAttacks',int, 'The maximum number of attacks this fish has per turn'),
    Variable('attacksLeft', int, 'The number of attacks a fish has left'),
    Variable('range',int,'The attack range of the fish'),
    Variable('species',str,'The fish species'),
    ],
  functions=[
    Function('move', [Variable('x', int), Variable('y', int)], 
    doc='Command a fish to move to a specified position'),
    Function('pickUp', [Variable('x', int), Variable('y', int), Variable('weight', int)],
    doc='Command a fish to pick up some trash at a specified position'),
    Function('drop', [Variable('x', int), Variable('y', int), Variable('weight', int)],
    doc='Command a fish to drop some trash at a specified position'),
    Function('attack', [Variable('x', int), Variable('y', int)],
    doc='Command a fish to attack another fish at a specified position'),
   ]
  )

move = Animation('move',
  data=[
    Variable('actingID', int),
    Variable('fromX', int),
    Variable('fromY', int),
    Variable('toX', int),
    Variable('toY', int),
  ],
  )
  
playerTalk = Animation('playerTalk',
  data=[
    Variable('actingID', int),
    Variable('message', str),
  ],
)

attack = Animation('attack',
  data=[
    Variable('actingID', int),
    Variable('targetID', int),
  ],
)

spawn = Animation('spawn',
  data=[
    Variable('x', int),
    Variable('y', int),
    Variable('species',str),
  ],
)

pickUp = Animation('pickUp',
  data=[
    Variable('x', int),
    Variable('y', int),
    Variable('actingID', int),
    Variable('amount',int),
  ],
)

drop = Animation('drop',
  data=[
    Variable('x', int),
    Variable('y', int),
    Variable('actingID', int),
    Variable('amount',int),
  ],
)

death = Animation('death',
  data=[
    Variable('actingID', int)
  ],
)




