class IStow(object):
   def __init__(self, aPackageDir, aPackageName, aTargetDir, aOptions):
      self.packageDir = aPackageDir
      self.packageName = aPackageName
      self.targetDir = aTargetDir
      self.options = aOptions
   
   def run(self):
      pass

# TODO: make this use abc
