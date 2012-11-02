from django.shortcuts import render_to_response
from django.http import Http404
from django.template.context import RequestContext

from cv_translator.apps.translator.utilities import genurls, checkMM


def home(request):
    '''Controller for app home page
    
    '''
    try:
        # get my urls
        urls = genurls()
    except:
        raise Http404
      
    if request.method == 'POST':
        # grab the uploaded mindmap file
        mmfile = request.FILES['uploadedfile']
        # First check for any errors in the freemind mindmap   
        errors = checkMM(mmfile)
        if len(errors):
            return render_to_response('page/errors.html', {'urls': urls, 'errors': errors},
                                  context_instance=RequestContext(request))
        else:
            return render_to_response('page/home.html', {'urls': urls},
                                  context_instance=RequestContext(request))
          
    else:
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
