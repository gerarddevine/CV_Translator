from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                           
    # admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # home and about pages
    (r'^$','cv_translator.apps.translator.views.home', {}, 'home'),
    (r'^about/$','cv_translator.apps.translator.views.about', {}, 'about'),
)


if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
    (r'^static/(?P<path>.*)$', 
        'serve', {
        'document_root': settings.STATIC_ROOT,
        'show_indexes': True }),
    (r'^media/(?P<path>.*)$', 
        'serve', {
        'document_root': settings.MEDIA_ROOT,
        'show_indexes': True }),
    )
