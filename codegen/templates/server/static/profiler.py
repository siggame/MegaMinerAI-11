import aspects
import main
from game_app.match import Match

hp = None
game_count = 0

def wrapPrintHeap(func):
  def inner(*args):
    heap = hp.heap()
    print heap
    print heap.more
    return func(*args)

  return inner

def incrementCount(func):
  def inner(*args, **kwargs):
    global game_count
    game_count += 1
    print "Game count: %s" % game_count
    print main.GameApp.games
    return func(*args, **kwargs)
  return inner

def decrementCount(func):
  def inner(*args, **kwargs):
    global game_count
    game_count -= 1
    print "Game count: %s" % game_count
    return func(*args, **kwargs)
  return inner

def install():
  global hp
  from guppy import hpy
  hp = hpy()

  aspects.wrap_function(Match.__init__, incrementCount)
  aspects.wrap_function(Match.__del__, decrementCount)
