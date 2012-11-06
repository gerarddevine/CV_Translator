from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext

from cv_translator.apps.translator.forms import MMForm
from cv_translator.apps.translator.utilities import genurls
from cv_translator.apps.translator.mindmap import checkMM, translateMM


def home(request):
    '''Controller for app home page
    
    Acts as the mindmap file upload page. A user can decide whether or not to 
    ignore any warnings in the mindmap (i.e. only errors will halt translation 
    to xml)    
    '''
  
    try:
        # get my urls
        urls = genurls()
    except:
        raise Http404
      
    if request.method == 'POST':
        mmform = MMForm(request.POST, request.FILES)
        if mmform.is_valid():
            # Grab the uploaded mindmap file
            mmfile = request.FILES['uploadedfile']
            # Check for any warnings/errors in the freemind mindmap   
            errors, warnings = checkMM(mmfile) 
            # Are warnings to be ignored?
            igWarnings = mmform.cleaned_data['igWarnings']
            
            if errors or (warnings and not igWarnings):   # generate an error/warnings report page
                return render_to_response('page/report.html', {'urls': urls, 
                                                               'errors': errors, 
                                                               'warnings': warnings}, 
                                       context_instance=RequestContext(request))
                
            else: #continue to translation
                translation = translateMM(mmfile)
                
                mimetype='application/xml'
                return HttpResponse(translation, mimetype)
                #return render_to_response('page/report.html', {'urls': urls, 
                #                                               'translation': translation}, 
                #                       context_instance=RequestContext(request))
                 
        else:
            # TODO: Need to put in better handling here
            return HttpResponseRedirect(urls['home'])
    else:
        mmform = MMForm()      
    
    return render_to_response('page/home.html', {'urls': urls, 'mmform': mmform},
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
