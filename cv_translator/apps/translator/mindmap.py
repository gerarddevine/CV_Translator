import re
import os
from lxml import etree

#get location of this directory for path setting
thisDir = os.path.dirname(__file__)
 
  
def checkMM(mmfile):
    ''' Validates a native freemind mindmap
    
    Check that the file is valid and return an error list
    '''
    
    #pull in the xsl transformation file
    XSLFileName = os.path.join(thisDir, 'xslt', 'mmcheck_0.9.0_bdl.xsl')
    #replace the _bdl string
    #foutname = str(mmfile).replace(".mm", ".xml")
    #set the fpre file
    fpre = open(os.path.join(thisDir,'xslt', str(mmfile)+'.pre'), 'w')
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
    transform(xml_input)    
    errorlog = transform.error_log
    
    #cleanup of temporary files
    os.remove(fpre.name)
    
    # separate out warnings and errors
    errorlist = []
    warninglist = []
    for entry in errorlog:
      if entry.message.startswith('*ERROR'):
        errorlist.append(entry.message.replace('*ERROR',''))
      if entry.message.startswith('*WARNING'):
        warninglist.append(entry.message.replace('*WARNING',''))
        
    #return the collection of errors and warnings
    return errorlist, warninglist
    

    