from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'default.views.start'),
    url(r'^wik$', 'default.views.wiki'),
    url(r'^kalender$', 'default.views.kalender'),

    url(r'^eval$', 'eval.views.home'),
    url(r'^eval/vorlesung/(?P<vl_id>\d+)', 'eval.views.vl'),
    url(r'^eval/kommentare/(?P<vl_id>\d+)', 'eval.views.comments'),
    url(r'^eval/editbogen/(?P<vl_id>\d+)/(?P<bogen_id>\d+)', 'eval.views.editbogen'),
    url(r'^eval/editbogen/(?P<vl_id>\d+)', 'eval.views.editbogen'),

    url(r'^rhp$', 'rhp.views.list'),
    url(r'^rhp/(?P<rhp_id>\d+)/artikel/(?P<artikel_id>\d+)', 'rhp.views.artikel'),
    url(r'^rhp/(?P<rhp_id>\d+)/artikel', 'rhp.views.artikel'),
    url(r'^rhp/move/(?P<artikel_id>\d+)/(?P<direction>\w+)', 'rhp.views.move'),
    url(r'^rhp/export/(?P<rhp_id>\d+)', 'rhp.views.export'),
    
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.djhtml'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^import/$', 'eval.views.imports'),
                       
    
)
