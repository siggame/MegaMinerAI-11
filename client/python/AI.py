#-*-python-*-
from BaseAI import BaseAI
from GameObject import *


class AI(BaseAI):
  """The class implementing gameplay logic."""

  speciesIndex = { "SEA_STAR": 0, "SPONGE": 1, "ANGELFISH":2, "CONESHELL_SNAIL":3, "SEA_URCHIN":4, "OCTOPUS":5, "TOMCOD":6, "REEF_SHARK":7, "CUTTLEFISH":8, "CLEANER_SHRIMP":9, "ELECTRIC_EEL":10, "JELLYFISH":11 }

  @staticmethod
  def username():
    return "Shell AI"

  @staticmethod
  def password():
    return "password"

  ##This function is called once, before your first turn
  def init(self):
    pass

  ##This function is called once, after your last turn
  def end(self):
    pass

  ##This function is called each time it is your turn
  ##Return true to end your turn, return false to ask the server for updated information
  def run(self):
    return 1

  def __init__(self, conn):
    BaseAI.__init__(self, conn)
