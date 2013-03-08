from structures import *

def install(data):
  data['Player'].addData([Variable('time', float, 'Time remaining, updated at start of turn')])
