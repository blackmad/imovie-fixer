#!/usr/bin/python

# plistlib only appears to have useful functionality in python3
# import plistlib
import sys
import shutil
import os
from optparse import OptionParser
import subprocess
from xml.dom import minidom 


parser = OptionParser()
parser.add_option('-i', dest='input')
parser.add_option('-o', dest='outputDir')
parser.add_option('--old', dest='oldDir')
(options, args) = parser.parse_args()

backupFile = options.input + '.backup'
if not os.path.exists(backupFile):
  shutil.copyfile(options.input, backupFile)

xmlFile = options.input + '.xml'
if not os.path.exists(xmlFile):
   subprocess.call(['plutil', '-convert', 'xml1', '-o', xmlFile, options.input])

if options.outputDir and not os.path.exists(options.outputDir):
  os.mkdir(options.outputDir)

dom = minidom.parse(xmlFile)

def text(i):
  return " ".join(t.nodeValue for t in i.childNodes if t.nodeType==t.TEXT_NODE)

for node in dom.getElementsByTagName('string'):
  string = text(node)

  # some lines look like this for some reason
  #                 <string>/Users/blackmad/Desktop/try2/018.jpg - 180845192 - 0</string>
  parts = string.split(' - ')
  maybeFile = os.path.expanduser(parts[0])
  if os.path.exists(os.path.expanduser(string)):
    parts = [os.path.expanduser(string),]
    maybeFile = parts[0]

  if os.path.exists(maybeFile) or (options.oldDir and maybeFile.startsWith(options.oldDir)):
    basename = os.path.basename(maybeFile)
    dest = os.path.join(options.outputDir, basename)
    if not os.path.exists(dest) and os.path.exists(maybeFile):
      shutil.copyfile(maybeFile, dest)
      print 'moving %s to %s ' % (maybeFile, dest)
    else:
      print 'updating %s to %s' % (maybeFile, dest)
    newText = ' - '.join([os.path.abspath(dest),] + parts[1:])

    node.firstChild.replaceWholeText(newText)

outputFile = options.input + '-updated.xml'
dom.writexml(open(outputFile, 'w'))
subprocess.call(['plutil', '-convert', 'binary1', '-o', options.input, outputFile])




