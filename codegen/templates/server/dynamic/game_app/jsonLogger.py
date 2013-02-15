import json
import gzip
import os

class JsonLogger:

  def __init__(self, logPath):
    self.logPath = logPath + ".json.gz"
    if (not os.path.exists("logs/")):
      os.mkdir("logs/")
    if (os.path.exists(self.logPath)):
      os.remove(self.logPath)
    self.file = gzip.open(self.logPath, "wb")
  
  def writeLog(self, dictLog):
    self.file.write(json.dumps(dictLog))
    self.file.close()
