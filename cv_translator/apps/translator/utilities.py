import libxml2
import libxslt
import re
import os
import sys
from lxml import etree

from StringIO import StringIO

from django.core.urlresolvers import reverse

#get location of this directory for path setting
thisDir = os.path.dirname(__file__)


# set up generic urls
def genurls():
    '''Creates a dictionary of general URL reversals
    
    '''
    
    urls = {}
    urls['home'] = reverse('home', args=())
    urls['about'] = reverse('about', args=())
    
    return urls
  
  
def checkMM(mmfile):
    ''' Validates a native freemind mindmap
    
    Check that the file is valid and return an error list
    '''
    
    #pull in the xsl transformation file
    XSLFileName = os.path.join(thisDir, 'mmcheck_0.9.0_bdl.xsl')
    #replace the _bdl string
    #foutname = str(mmfile).replace(".mm", ".xml")
    #set the fpre file
    fpre = open(os.path.join(thisDir, str(mmfile)+'.pre'), 'w')
    #begin reading through each line in the mm file, and....
    for line in mmfile:
        # make necessary mods to richcontent symbols
        if re.match("^<richcontent", line):
            line = line.replace('[','<')
            line = line.replace(']','>') 
            #write edited line to pre file 
        fpre.write(line)
    #close the pre file
    fpre.close()
    
    # pull in the xml and xslt files
    xml_input = etree.parse(fpre.name)
    xslt_root = etree.parse(XSLFileName)
    #set up the transformation
    transform = etree.XSLT(xslt_root)
    
    # make the transformation and collect any errors
    result = transform(xml_input)    
    errorlog = transform.error_log
    
    #return the collection of errors
    return errorlog
    

    