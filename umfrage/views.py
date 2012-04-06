# -*- coding: utf-8 -*-
from django.http import Http404
from django.contrib import messages
from extensions.templates import TemplateHelper
from jinja2 import Environment,  PackageLoader
from umfrage.models import Umfrage, Option, Vote
from django.contrib.auth.decorators import login_required

t = TemplateHelper('umfrage')

@login_required
def list(request):
    return t.render('list.djhtml', {'umfragen': Umfrage.objects.all(),}, req=request)

@login_required
def umfrage(request, umfrage_id):
    try:
        u = Umfrage.objects.get(pk=umfrage_id)
    except Umfrage.DoesNotExist:
        raise Http404

    if request.POST and request.is_ajax():
        reqdata = request.POST
        for key, value in reqdata.iteritems():
            try:
                option_id    = int(key)
                print key, value
                option       = Option.objects.get(pk=option_id)

                if len(Vote.objects.filter(user=request.user, option=option)):
                    response = {'success': False}
                    message.error(request, 'Bereits gevotet für Option' + option.titel)
                    break
                
                vote         = Vote()
                vote.option  = option
                vote.user    = request.user
                vote.umfrage = option.umfrage
                vote.choice  = value
                vote.save()
                
            except ValueError:
                pass
            
            response = {'success':True}

        if response['success']:
            messages.success(request, "Erfolgreich eingetragen")
            
        return t.ajax(response)
    else:
        return t.render('umfrage.djhtml', {
                'umfrage': u,
                'optionen': u.optionen.all(),
                'votes': u.votes.all(),
                'currentuser': request.user,
                'choices': {-1: 'Nein', 0:'Vielleicht', 1:'Ja'}
                }, req=request)
