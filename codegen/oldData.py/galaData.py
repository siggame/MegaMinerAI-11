# -*- coding: iso-8859-1 -*-
from structures import *

aspects = ['timer']

gameName = "Galapagos"

globals = [
  Variable('turnNumber', int, 'How many turns it has been since the
beginning of the round'),
  Variable('playerID', int, 'Player Number; either 0 or 1'),
  Variable('gameNumber', int, 'What game number this is for the server'),
  Variable('mapWidth', int, 'The width of the map'),
  Variable('mapHeight', int, 'The height of the map'),
  Variable('healthPerBreed', int, 'The amount of energy required from -each-
  creature in order to breed.'),
  Variable('healthPerMove', int, 'The amount of energy required to move.'),
  Variable('healthPerTurn', int, 'The amount of energy lost after each of
  your turns.'),
  Variable('baseHealth', int, 'The base amount of health that each creature
  starts with'),
]

constants = [
]

playerData = [
]

playerFunctions = [
  Function('talk', [Variable('message', str)], doc='Allows a player to
display messages on the screen'),
]

Mappable = Model('Mappable',
  data=[
    Variable('x', int, 'X position of the object'),
    Variable('y', int, 'Y position of the object'),
  ],
  doc="A mappable object!",
)

Plant = Model('Plant',
  parent=Mappable,
  data=[
    Variable('size', int, 'The size of the plant'),
    Variable('growthRate', int, 'The total number of turns it takes this
plant to grow in size.'),
    Variable('turnsUntilGrowth', int, 'The number of turns left until this
plant will grow again.'),
  ],
  doc="A basic plant!",
)

Creature = Model('Creature',
  parent=Mappable,
  data=[
    Variable('owner', int, 'The owner of the creature'),
    Variable('maxHealth', int, 'The maximum amount of health this creature
can have'),
    Variable('currentHealth', int, 'The current amount of health that this
creature has.'),
    Variable('energy', int, 'The energy level of the creature. This
increases your max health'),
    Variable('carnivorism', int, 'The carnivore level of the creature. This
increases damage to other other creatures and health restored on kill.'),
    Variable('herbivorism', int, 'The herbivore level of the creature. This
increases health restored from eating plants'),
    Variable('speed', int, 'The speed of the creature. This determines how
many times a creature can move in one turn.'),
    Variable('movementLeft', int, 'The amount of moves this creature has
left this turn.'),
    Variable('defense', int, 'The defense of the creature. This reduces the
amount of damage this creature takes from being eaten.'),
    Variable('canEat', int, 'Indicated whether or not this creature can eat
this turn.'),
    Variable('canBreed', int, 'Indicated whether or not this creature can
breed this turn.'),
    Variable('parentID', int, 'ID of the creature that gave birth to this
one.'),
  ],
  functions=[
    Function('move', [Variable('x', int), Variable('y', int)],
    doc='Command a creature to move to a specified position'),
    Function('eat', [Variable('x', int), Variable('y', int)],
    doc='Eat plant or creature at input location'),
  ],
  doc="A basic creature!",
)

Creature.addFunctions(
  [
    Function ('breed', [Variable('mate', Creature)],
    doc='Breed with target adjacent creature. New creature will be spawned
under the calling creature.'),
  ]
)

playerTalk = Animation('playerTalk',
  data=[
    Variable('actingID', int),
    Variable('message', str),
  ],
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

eat = Animation('eat',
  data=[
    Variable('actingID', int),
    Variable('targetID', int),
  ],
)

death = Animation('death',
  data=[
    Variable('actingID', int)
  ],
)

breed = Animation('breed',
  data=[
    Variable('actingID', int),
    Variable('targetID', int),
    Variable('childID', int)
  ],
)
