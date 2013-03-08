# -*- coding: iso-8859-1 -*-
from structures import *

aspects = ['timer']

Player = Model('Player', data= [Variable('playerName',str, "Player's Name"),Variable('gold',int, "Player's Gold")])

Mappable = Model('Mappable',
  data = [ Variable('x', int, 'The X position of this object.  X is horizontal, with 0,0 as the top left corner'),
    Variable('y', int, 'The Y position of this object.  Y is vertical, with 0,0 as the top left corner'),
    ],
  doc = 'An object that exists on the grid',
  type = 'virtual'
  )

Unit = Model('Unit',
  parent = Mappable,
    data = [Variable('owner', int, 'Represents the owner of the unit.'),
    Variable('health', int, 'Current health of the unit'),
    Variable('strength', int, 'Attacking strength of the unit (Each point of strength deals 1 health of damage)'),
    Variable('movesLeft', int, 'Displays the remaining moves for this unit this turn'),
    Variable('attacksLeft', int, 'Displays the remaining attacks for this unit this turn'),
    Variable('gold', int, 'Amount of gold carried by the unit.'),
    ],
  doc = 'Generic Unit',
  functions = [
    Function('move',
      arguments = [Variable('x', int, 'The x coordinate of where the unit wishes to move'), 
	    Variable('y', int, 'The Y coordinate of where the unit wishes to move')],
      result = bool,
      doc = 'Move the unit to the designated X and Y coordinates if possible'
    ),
    Function('talk',
      arguments = [Variable('message', str, 'The message that the unit should say')],
      doc = 'Allows a unit to display a message to the screen.'
    ),
  ],
  type = 'virtual'
)

Unit.functions.append(Function('attack',
      arguments = [Variable('Target', Unit, 'The unit you wish to attack')],
      result = bool,
      doc = 'Attempt to attack the input target if possible'
      ))


Pirate = Model('Pirate',
  parent = Unit,
  doc = 'A basic pirate. These units are bound to land unless aboard a ship. they can pickup and drop treasure as well as build ports and fight other pirates.',
  functions = [
    Function('pickupTreasure',
      arguments = [Variable('amount', int, 'The amount of gold you wish the pirate to pick up')],
      doc = 'Allows the pirate to pickup treasure on the ground.'
    ),
    Function('dropTreasure',
      arguments = [Variable('amount', int, 'The amount of gold you wish this pirate to drop')],
      doc = 'Allows the pirate to drop treasure they are carrying.'
    ),
    Function('buildPort',
      arguments = [],
      result = bool,
      doc = 'Pirate builds a port on a land tile with water tile adjacent. Cannot be within three spaces of another port!'
    )
  ]
)


Ship = Model('Ship',
  parent = Unit,
  doc = 'A basic ship. They can only travel by sea and attack other ships. Whenever the ship moves, any pirates on his tile go with it',
)

Port = Model('Port',
  parent = Mappable,
  data = [ Variable('owner', int, 'The ownder of the port'),
    ],
  doc = 'A basic port. The port can create new pirates and ships and is used when pirates need to deposit money.',
  functions = [ 
    Function('createPirate',
	  arguments = [],
	  result = bool,
	  doc = 'Creates a Pirate at the calling Port'
	),
    Function('createShip',
	  arguments = [],
	  result = bool,
	  doc = 'Creates a Ship at the calling Port'
	),
  ]
)

Tile = Model('Tile',
  parent = Mappable,
  data = [ Variable('type', float, 'land = 0, water = 1'),
    ],
  doc = 'A basic tile',
)

Treasure = Model('Treasure',
  parent = Mappable,
  data = [ Variable('gold', int, 'The amount of gold currently with this treasure'),
    ],
  doc = 'This is the source of your wealth. When dropped on the ground it will build interest baed on its distance to pirates, if dropped on a port it is added to your ooverall wealth',
)

move = Animation("Move",
  data = [Variable("unit", Unit), Variable("x", int), Variable("y",int)]
  )

shipAttack = Animation("Shipattack",
  data = [Variable("attacker", Unit), Variable("attackx", int), Variable( "attacky", int )]
  )
 
pirateAttack = Animation("Pirateattack",
  data = [Variable("attacker", Unit), Variable("attackx", int), Variable( "attacky", int )]
  )
   
talk = Animation("Talk",
  data = [Variable("speaker", Unit), Variable("message", str)]
  ) 
    

globals = [
  Variable('turnNumber', int, 'How many turns it has been since the beginning of the game'),
  Variable('playerID', int, 'Player Number; either 0 or 1 (0 is player 1, 1 is player 2)'),
  Variable('gameNumber', int, 'What number game this is for the server'),
  Variable('pirateCost', int, 'The cost of a pirate'),
  Variable('shipCost', int, 'The cost of a ship'),
  Variable('portCost', int, 'The cost to build a new port'),
  Variable('mapSize', int, 'The boards width and height'),
  ]

constants = [
  ]
