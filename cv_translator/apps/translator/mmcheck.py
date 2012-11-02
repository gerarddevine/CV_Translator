#! /usr/bin/env python
from optparse import OptionParser
import re
import sys
import libxml2
import libxslt
import os

usage = "usage: %prog [options] mindmap_[flat,bdl].mm"
version = "1.0"
parser = OptionParser(usage)
parser.add_option("-n", "--nopreprocess",
                  action="store_false", dest="preprocess", default=True,
                  help="preprocess mindmaps to turn '[]' to '<>'")
parser.add_option("-k", "--keep",
                  action="store_true", dest="keep", default=False,
                  help="don't delete any temporary files")
parser.add_option("-w", "--warning",
                  action="store_true", dest="warning", default=False,
                  help="output warnings from checker")
parser.add_option("-f", "--flat",
                  action="store_true", dest="flat", default=False,
                  help="parse a flattened mindmap rather than a bundled one")
parser.add_option("-v", "--version", dest="version", default='0.8.1',
                  help="Freemind version that mindmap was produced with (default = 0.8.1)")
(options, args) = parser.parse_args()

if len(args) < 1 or len(args) > 2:
  parser.error("incorrect number of arguments")

if options.flat:
  if not(args[0].endswith("_flat.mm")):
     parser.error("expecting input file with name mindmap_flat.mm. Do not use the -f option is you want to parse a mindmap_bdl.mm file.")
  foutname=args[0].replace("_flat.mm",".xml")
  XSLFileName="mmcheck_flat.xsl"
else:
  if not(args[0].endswith("_bdl.mm")):
     parser.error("expecting input file with name mindmap_bdl.mm. Use the -f option is you want to parse a mindmap_flat.mm file.")
  foutname=args[0].replace("_bdl.mm",".xml")
  # Check which xsl file to use depending on freemind version 
  if options.version == '0.9':
    XSLFileName="mmcheck_0.9.0_bdl.xsl"
  elif options.version == '0.8.1':
    XSLFileName="mmcheck_bdl.xsl"
  else:
    parser.error("Freemind version is not recognised. Leave blank for default version (0.8.1) or use -v 0.9")

try:
  fin = open(args[0], 'r')
except IOError, (errno, strerror):
  print "I/O error(%s) for file %s: %s" % (errno, args[0], strerror)
  sys.exit(1)

if options.preprocess:
  fpre = open(args[0]+'.pre', 'w')
  print "preprocessing mm xml from %s to %s" % (fin.name,fpre.name)
  for line in fin:
    if options.version == '0.8.1':
      # replacements in the event of freemind version 0.8.1
      if re.match("^<text>",line):
        line=line.replace('[','<')
        line=line.replace(']','>')
    elif options.version == '0.9':
      # replacements in the event of freemind version 0.9.0
      if re.match("^<richcontent",line):
        line=line.replace('[','<')
        line=line.replace(']','>')
    fpre.write(line)
  fpre.close()
else:
  fpre=fin

if (options.warning):
  warn="'yes'"
else:
  warn="'no'"

print "checking mm xml from file %s" % fpre.name
styledoc = libxml2.parseFile("xsl/"+XSLFileName)
style = libxslt.parseStylesheetDoc(styledoc)
doc = libxml2.parseFile(fpre.name)
print "Start of errors"
sys.stdout.flush()
result = style.applyStylesheet(doc,{"Warning" : warn, "CheckConstraints" : "'yes'" })
#result = style.applyStylesheet(doc,{"Warning" : warn, "CheckConstraints" : "yes", "CompLen" : "25"})

print "End of errors"
style.freeStylesheet()
doc.freeDoc()
result.freeDoc()

if not(options.keep) and options.preprocess:
  print "removed temporary file %s" % fpre.name
  os.remove(args[0]+'.pre')
