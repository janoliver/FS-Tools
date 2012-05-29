#!/usr/bin/python2
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
admin.autodiscover()

urlpatterns = patterns(
    '',

    # Login / Logout
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.djhtml'}),
    url(r'^accounts/logout/$',
        'django.contrib.auth.views.logout_then_login'),

    # Die folgenden Routen sind statische Seiten, für die generische Views
    # verwendet werden.
    url(r'^$', login_required(TemplateView.as_view(template_name="start.djhtml"))),
    url(r'^wik$', login_required(TemplateView.as_view(template_name="wiki.djhtml"))),
    url(r'^kalender$', login_required(TemplateView.as_view(template_name="kalender.djhtml"))),

    # Die Evaluations App
    url(r'^eval$', 'eval.views.home'),
    url(r'^eval/vorlesung/(?P<vl_id>\d+)', 'eval.views.vl'),
    url(r'^eval/einverst/(?P<vl_id>\d+)', 'eval.views.einverst'),
    url(r'^eval/kommentare/(?P<vl_id>\d+)', 'eval.views.comments'),
    url(r'^eval/editbogen/(?P<vl_id>\d+)/(?P<bogen_id>\d+)',
        'eval.views.editbogen'),
    url(r'^eval/einverst/toggle_single/(?P<typ>\w+)/(?P<vl_id>\d+)/(?P<person_id>\d+)',
        'eval.views.einverst_single'),
    url(r'^eval/einverst/toggle_forever/(?P<vl_id>\d+)/(?P<person_id>\d+)',
        'eval.views.einverst_forever'),
    url(r'^eval/editbogen/(?P<vl_id>\d+)', 'eval.views.editbogen'),
    url(r'^eval/export/(?P<vlu_id>\d+)', 'eval.views.export_einverst'),

    # DIe RHP App
    url(r'^rhp$', 'rhp.views.list'),
    url(r'^rhp/(?P<rhp_id>\d+)/artikel/(?P<artikel_id>\d+)',
        'rhp.views.artikel'),
    url(r'^rhp/(?P<rhp_id>\d+)/artikel', 'rhp.views.artikel'),
    url(r'^rhp/move/(?P<artikel_id>\d+)/(?P<direction>\w+)',
        'rhp.views.move'),
    url(r'^rhp/export/(?P<rhp_id>\d+)', 'rhp.views.export'),

    # Die Umfrage App
    url(r'^umfrage$', 'umfrage.views.list'),
    url(r'^umfrage/(?P<umfrage_id>\d+)', 'umfrage.views.umfrage'),

    # Die PPP App
    url(r'^ppplist$', 'ppp.views.list'),
    url(r'^ppp/(?P<ppp_id>\d+)', 'ppp.views.details'),
    url(r'^ppp/matr/(?P<ppp_id>\d+)', 'ppp.views.matrikelnr'),
    url(r'^ppp/delmatr/(?P<ppp_id>\d+)', 'ppp.views.matrikelnr_del'),
    url(r'^ppp$','ppp.views.abstimmen'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
    )

