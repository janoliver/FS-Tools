#!/usr/bin/python2
# -*- coding: utf-8 -*-
from django.http import Http404
from extensions.templates import TemplateHelper
from django.contrib.auth.decorators import login_required
from rhp.models import Rhp
from eval.models import Vlu

t = TemplateHelper('default')


@login_required
def start(request):
    vlu = Vlu.objects.get(pk=1)
    rhp = Rhp.objects.get(pk=1)
    print vlu.vlu_start, rhp.vlu.vlu_start
    return t.render('start.djhtml')


@login_required
def wiki(request):
    return t.render('wiki.djhtml')


@login_required
def kalender(request):
    return t.render('kalender.djhtml')
