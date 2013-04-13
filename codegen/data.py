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
  Variable ('maxReefHealth', int, "The maximum and initial health of each player's reef."),
  Variable('boundLength', int, 'How far the shared zone extends from the center'),
  Variable('turnNumber', int, 'How many turns it has been since the beginning of the game'),
  Variable('playerID', int, 'Player Number; either 0 or 1'),
  Variable('gameNumber', int, 'What number game this is for the server'),
  Variable('mapWidth', int, 'How wide the map is'),
  Variable('mapHeight', int, 'How high the map is'),
  Variable('trashAmount',int, 'Amount of trash in the game'),
  Variable('currentSeason', int, 'Determines what season it is. Species availability will change with passing season'),
  Variable('seasonLength',int, 'Describes how long a season lasts'),
  Variable('healPercent', int, 'Percentage of max health a fish gets back whenever it is healed, by either cove or other fish'),
  Variable('maxFood', int, "The maximum amount of food a player can have."),
]

Tile = Model('Tile',
  parent = Mappable,
  data = [
    Variable('trashAmount', int, 'The amount of trash on this tile'),
    Variable('owner', int , 'The owner of the tile if it is part of a cove'),
    Variable('hasEgg',int, 'Determines of a fish is set to spawn on this cove'),
    Variable('damages',int, 'Determines which player the trash on this tile will hurt'),
    ],
  doc='Represents a single tile on the map, can contain some amount of trash or be a cove (spawn point).',
  permanent = True,
  )

Species = Model('Species',
  data = [
    Variable('name', str, 'The name of this species'),
    Variable('speciesNum', int, 'The number assigned to the species, unique to each.'),
    Variable('cost', int, 'The amount of food it takes to raise this fish'),
    Variable('maxHealth', int, 'The maximum health of this fish'),
    Variable('maxMovement', int, 'The maximum number of movements in a turn'),
    Variable('carryCap', int, 'The total weight the fish can carry'),
    Variable('attackPower', int, 'The power of the fish\'s attack'),
    Variable('range',int,'The attack range of the fish'),
    Variable('maxAttacks',int,'Maximum number of times this unit can attack per turn'),
    Variable('season',int, 'Determines what season this species will be spawnable in'),
    ],
  functions=[
    Function('spawn',[Variable('tile',Tile)],
    doc='Have a new fish spawn and join the fight! Select which tile you want the fish to spawn on'),
    ],
  doc='This class describes the characteristics for each type of fish. A species will only be available for so long, and new species will become available as a match progreses. ',
  plural='SpeciesList',
  permanent = True,
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
    Variable('maxAttacks',int, 'The maximum number of attacks this fish has per turn'),
    Variable('attacksLeft', int, 'The number of attacks a fish has left'),
    Variable('range', int,'The attack range of the fish'),
    Variable('species', int,'The index of the fish species.'),
    ],
  functions=[
    Function('move', [Variable('x', int), Variable('y', int)],
    doc='Command a fish to move to a specified position'),
    Function('pickUp', [Variable('tile',Tile), Variable('weight', int)],
    doc='Command a fish to pick up some trash at a specified position'),
    Function('drop', [Variable('tile',Tile), Variable('weight', int)],
    doc='Command a fish to drop some trash at a specified position'),
   ],
  doc='This is your primary unit for Reef. It will perform all of your major actions (pickup, attack, move, drop). It stats are based off of its species',
  plural = 'Fishes'
 )

Fish.addFunctions([Function('attack',[Variable('target',Fish)],
  doc='Command a fish to attack a target'
  )])

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
    Variable('playerID', int),
    Variable('x', int),
    Variable('y', int),
    Variable('species',str),
  ],
)

pickUp = Animation('pickUp',
  data=[
    Variable('actingID', int),
    Variable('targetID', int),
    Variable('x', int),
    Variable('y', int),
    Variable('amount',int),
  ],
)

drop = Animation('drop',
  data=[
    Variable('actingID', int),
    Variable('targetID', int),
    Variable('x', int),
    Variable('y', int),
    Variable('amount',int),
  ],
)

death = Animation('death',
  data=[
    Variable('actingID', int)
  ],
)



