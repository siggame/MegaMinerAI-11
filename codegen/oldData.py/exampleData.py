# -*- coding: iso-8859-1 -*-
from structures import *

# Informs the codegen if it should include turn timing
aspects = ['timer']

# Variables the server needs to send the client each game
globals = [
  Variable('turnNumber', int, 'How many turns it has been since the beginning of the game'),
  Variable('playerID', int, 'Player Number; either 0 or 1 (0 is player 1, 1 is player 2)'),
  Variable('gameNumber', int, 'What number game this is for the server'),
  ]

# Constants that are built directly into the client
constants = [
  ]

# Defines a player object, used to store information for each player, like score, gold, etc
Player = Model('Player',
  # Container holding all of the Player's variables 
  data = [
    Variable('playerName',str, "Player's Name"),
    ],
  # The documentation string for Player objects
  doc = 'Stores information about all of the players in the game',
  # Container holding all of the functions a Player can perform
  functions = [
    Function('talk',
      arguments = [Variable('message', str, 'The message that the player should say')],
      doc = 'Allows a player to display a message to the screen.'
      ),
    ]
  )

# Defines an Animation, which is sent to the visualizer to let it know something happened
talk = Animation("PlayerTalk",
  data = [
    Variable("speaker", Player), 
    Variable("message", str)
    ]
  )

Mappable = Model('Mappable',
  data = [
    Variable('x', int, 'The X position of this object.'),
    Variable('y', int, 'The Y position of this object.'),
    ],
  doc = 'An object that exists on the map',
  type = 'virtual'
  )

Unit = Model('Unit',
  parent = Mappable,
    data = [
      Variable('owner', int, 'Represents the owner of the unit.'),
      Variable('health', int, 'Current health of the unit'),
      Variable('strength', int, 'Amount of damage this unit does when attacking'),
      Variable('movesLeft', int, 'The remaining moves for this unit this turn'),
      Variable('attacksLeft', int, 'The remaining attacks for this unit this turn'),
      ],
  doc = 'Generic Unit',
  functions = [
    Function('move',
      arguments = [
        Variable('x', int, 'The x coordinate of where the unit wishes to move'), 
	      Variable('y', int, 'The Y coordinate of where the unit wishes to move')
	      ],
      result = bool,
      doc = 'Move the unit to the designated X and Y coordinates if possible'
    ),
    Function('talk',
      arguments = [Variable('message', str, 'The message that the unit should say')],
      doc = 'Allows a unit to display a message to the screen.'
    ),
  ],
)

Unit.addFunctions([
  Function('attack',
    arguments = [Variable('Target', Unit, 'The unit you wish to attack')],
    result = bool,
    doc = 'Attempt to attack the input target if possible'
    )
  ])


