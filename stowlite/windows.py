import itertools
import os
import os.path
import re
import subprocess
import sys

import stowlite.helper
import stowlite.istow

'''
Implements a behavior very similar to a small subset of GNU stow operations. It is sufficient for my needs when working on Windows.

If the name of any file or directoy in the stow directory matches one of the regular expressions in .stow-local-ignore, then it is ignored. If a directory is not ignored, then it is linked. There is no way to ignore certain files/directories in a linked directory. Please note that this is different from stow's normal behavior.
'''


class StowLiteWindows(stowlite.istow.IStow):
   def __init__(self, aPackageDir, aPackageName, aTargetDir, aOptions):
      super(StowLiteWindows, self).__init__(aPackageDir, aPackageName, aTargetDir, aOptions)
      self.stowDir = os.path.normpath(os.path.join(self.packageDir, '..'))
      self.localIgnoreFilename  = '.stow-local-ignore'
      self.globalIgnoreFilename = '.stow-global-ignore'
   
   def getLocalIgnoreRegexes(self):
      '''
      Return compiled regular expressions.
      '''
      tFilePath = os.path.normpath(os.path.join(self.packageDir, self.localIgnoreFilename))
      
      try:
         with open(tFilePath) as tFile:
            tLines = tFile.read().splitlines()
      except IOError as tException:
         tLines = []
      # TODO: remove: print tLines
      return [re.compile(tPattern) for tPattern in tLines]
   
   def getGlobalIgnoreRegexes(self):
      '''
      Return compiled regular expressions.
      '''
      return []
      
   def isFileOrDirIgnored(self, aFileOrDirPath, aIgnoreRegexes):
      for tRegexCompiled in aIgnoreRegexes:
         if tRegexCompiled.match(aFileOrDirPath):
            return True
      
      return False
      
   def getFilesAndDirsToLink(self):
      #tIgnoreRegexes = itertools.chain(self.getLocalIgnoreRegexes(), self.getGlobalIgnoreRegexes())
      tIgnoreRegexes = self.getLocalIgnoreRegexes() + self.getGlobalIgnoreRegexes()
      
      # TODO need to ignore stow's '.stow-local-ignore' and also my '.stowrc' etc.

      tFilesAndDirs = [os.path.join(self.packageDir, tElement) for tElement in os.listdir(self.packageDir)]
      tFilesAndDirsToLink = [tFile for tFile in tFilesAndDirs if not self.isFileOrDirIgnored(os.path.basename(tFile), tIgnoreRegexes)]
   
      return tFilesAndDirsToLink
   
   def makeLink(self, aFileOrDirPathSource, aDestinationDir):
      if not self.options.dryRun:
         print 'Making link for {} to {}'.format(aFileOrDirPathSource, aDestinationDir)
      else:
         print 'Would have hade link for {} to {}'.format(aFileOrDirPathSource, aDestinationDir)
         return
   
      if False:
      #if self.options.cygwin:
         pass
      else:
         tCommandTemplate = 'cmd /c mklink {tOptions} {tLinkName} {tTarget}'
      
         if os.path.isfile(aFileOrDirPathSource):
            tOptions = ''
         elif os.path.isdir(aFileOrDirPathSource):
            tOptions = '/D'
         else:
            raise Exception('Neither a file nor directory.')
         
         with stowlite.helper.cd(aDestinationDir):
            tCommand = tCommandTemplate.format(
               tOptions=tOptions,
               tLinkName=os.path.basename(aFileOrDirPathSource),
               tTarget=aFileOrDirPathSource)
            #print 'tCommand = ' + tCommand
            
            tDestinationFilePath = os.path.join(aDestinationDir, os.path.basename(aFileOrDirPathSource))
            if os.path.lexists(tDestinationFilePath):
               # If the destination already exists, delete it first.
               if os.path.isfile(tDestinationFilePath):
                  os.remove(tDestinationFilePath)
               elif os.path.isdir(tDestinationFilePath):
                  #os.rmdir(tDestinationFilePath)
                  # FIXME This causes some problems if the symlink is still there from the first run.
                  os.unlink(tDestinationFilePath)
               else:
                  raise Exception('Neither a file nor directory.')
            
            # Create the link.
            subprocess.check_call(tCommand, shell=True)


   def stowPackage(self):
      for tFileOrDir in self.getFilesAndDirsToLink():
         self.makeLink(tFileOrDir, self.targetDir)
   
   
   def run(self):
      #print 'package dir  = ' + self.packageDir
      #print 'package name = ' + self.packageName
      #print 'target dir   = ' + self.targetDir
      #print 'stow dir     = ' + self.stowDir
      
      self.stowPackage()
   
   
   def runOld(self):
      if self.options.dryRun:
         tExtraOptions = '--simulate'
      else:
         tExtraOptions = ''
         
      if self.options.cygwin:
         # 'mkshortcut' instead of 'mklink'
         pass
   
      try:
         tStowDir = os.path.normpath(os.path.join(self.packageDir, '..'))
      

         # TODO maybe 'shlex.split' and no 'shell=True'
         subprocess.check_output(tCommand, shell=True)
      except subprocess.CalledProcessError as tException:
         # TODO: shouldn't exit. probably just want to return a code or rethrow a different exception.
         sys.exit(tException)

# TODO exit gracefully if insufficient privileges
