#!/usr/bin/env python
import sys, os, os.path, signal
import jsshellhelper
from optparse import OptionParser
from subprocess import Popen, PIPE, STDOUT

# Uses jsshell https://developer.mozilla.org/en/Introduction_to_the_JavaScript_shell

class Minifier(object):
  toolsdir = os.path.dirname(os.path.abspath(__file__))

  def run(self, jsshell, filename):
    tmpFile = jsshellhelper.createEscapedFile(filename)

    cmd = [jsshell,
           '-f', os.path.join(self.toolsdir, 'jsmin.js'),
           '-f', os.path.join(self.toolsdir, 'cleaner.js'),
           '-f', tmpFile,
           '-e', "var input = __unescape_string(); print(jsmin('', input, 2));"]

    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = proc.communicate()

    if stdout:
      print stdout
    else:
      print stderr

    jsshellhelper.cleanUp(tmpFile)

def main():
    parser = OptionParser()
    options, args = parser.parse_args()

    if len(args) < 2:
        print >>sys.stderr, """Usage: %s <path to jsshell> <js file>""" % sys.argv[0]
        sys.exit(1)

    minifier = Minifier()
    minifier.run(args[0], args[1])

if __name__ == '__main__':
    main()
