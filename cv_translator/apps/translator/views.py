from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.template.context import RequestContext

from cv_translator.apps.translator.utilities import genurls
from cv_translator.apps.translator.mindmap import checkMM


def home(request):
    '''Controller for app home page
    
    '''
    try:
        # get my urls
        urls = genurls()
    except:
        raise Http404
    
    return render_to_response('page/home.html', {'urls': urls},
                              context_instance=RequestContext(request))


def about(request):
    '''Controller for app about page
    
    '''
    try:
        # get my urls
        urls = genurls()
    except:
        raise Http404
      
    return render_to_response('page/about.html', {'urls': urls},
                              context_instance=RequestContext(request))


def report(request):
    ''' Reporting page controller listing any errors or warnings
    
    '''
    try:
        # get my urls
        urls = genurls()
    except:
        raise Http404
      
    try:
        # Grab the uploaded mindmap file
        mmfile = request.FILES['uploadedfile']
        # First check for any warnings/errors in the freemind mindmap   
        errors, warnings = checkMM(mmfile)     
        # and return this to the report page   
        return render_to_response('page/report.html', {'urls':urls, 
                                                       'errors':errors, 
                                                       'warnings':warnings}, 
                                  context_instance=RequestContext(request))
        
    except:
        # This page should only be accessible by request=POST so return to home page
        # if not
        return HttpResponseRedirect(urls['home']) 