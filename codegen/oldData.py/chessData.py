# -*- coding: iso-8859-1 -*-
from structures import *

aspects = []

Piece = Model('Piece',
  data = [ Variable('owner', int, 'The owner of the piece'),
    Variable('file', int, 'The letter this piece is at (1-8)'),
    Variable('rank', int, 'The number this piece is at (1-8)'),
    Variable('hasMoved', int, '1=has moved, 0=has not moved'),
    Variable('type', int, 'The letter that describes this piece\'s type. K=King, Q=Queen, B=Bishop, N=Knight, R=Rook, P=Pawn'),
    ],
  doc = 'A chess piece',
  functions = [ Function('move', [Variable('file', int), Variable('rank', int), Variable('type', int) ] ) ],
  )
  
Move = Model('Move',
  data = [ Variable('fromFile', int, 'The initial file location'),
    Variable('fromRank', int, 'The initial rank location'),
    Variable('toFile', int, 'The final file location'),
    Variable('toRank', int, 'The final rank location'),
    Variable('promoteType', int, 'The type of the piece for pawn promotion. Q=Queen, B=Bishop, N=Knight, R=Rook'),
    ],
  doc = 'A chess move',
  )
  
move = Animation('move',
  data = [ Variable('fromFile', int),
    Variable('fromRank', int),
    Variable('toFile', int),
    Variable('toRank', int),
    Variable('promoteType', int),
    ],
  )

globals = [
  Variable('turnNumber', int, 'How many turns it has been since the beginning of the game'),
  Variable('playerID', int, 'Player Number; either 0 or 1'),
  Variable('gameNumber', int, 'What number game this is for the server'),
  Variable('TurnsToStalemate', int, 'How many turns until the game ends because no pawn has moved and no piece has been taken'),
  ]

constants = [
  Variable('player0Name', str, 'Player 0\'s name'),
  Variable('player1Name', str, 'Player 1\'s name'),
  ]

import timerAspect
timerAspect.install()
