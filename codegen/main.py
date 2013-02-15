#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
import structures
import argparse
import runpy
import os.path, os
import conversions
import copy

def insertModel(list, model):
  if model.parent and model.parent not in list:
    insertModel(list, model.parent)
  if model not in list:
    list.append(model)

def parseData(data):
  aspects = data['aspects']
  data['Player'] = structures.Model("Player", data=[structures.Variable("playerName", str, "Player's Name")])
  if 'timer' in aspects:
    import timerAspect
    timerAspect.install(data)
  data['Player'].addData(data['playerData'])
  data['Player'].addFunctions(data['playerFunctions'])
  models = []
  globals = data['globals']
  constants = data['constants']
  animations = []
  gameName = data['gameName']

  for i in data.values():
    if isinstance(i, structures.Model):
      insertModel(models, i)
    elif isinstance(i, structures.Animation):
      animations.append(i)
  return {'models':models, 'globals':globals, 'constants':constants, 'animations':animations, 'aspects':aspects, 'gameName':gameName}



if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Run The Codegen To Automatically Generate Some Codez')
  parser.add_argument('-d', '--data', dest='dataPyPath', default='./data.py', help='The Path To data.py')
  parser.add_argument('-o', '--output', dest='outDir', default='./output', help='The output of the codegen.')
  parser.add_argument('-t', '--template', dest='templatePath', default='./templates', help='The location of the templates')

  args = parser.parse_args()

  data = runpy.run_path(args.dataPyPath)

  objects = parseData(data)
  conversions.addModels(data)
  output = args.outDir
  templates = args.templatePath

  import writers
  g = writers.__dict__
  for module in os.listdir(templates):
    modulePath = os.path.join(templates, module)
    outPath = os.path.join(output, module)
    writerPath = os.path.join(modulePath, 'writer.py')
    if os.path.exists(writerPath):
        m = runpy.run_path(writerPath, g)
        w = m['writer']()
        w.write(modulePath, outPath, copy.copy(objects))

  # rename the plugins/GAME_NAME dir to the game name, because at the moment folders can't be dynamically named
  try:
    os.rename(output + "/plugins/GAME_NAME", output + "/plugins/" + objects['gameName'].lower())
  except:
    print("Error renaming plugins dir")

