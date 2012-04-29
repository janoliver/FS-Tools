#!/usr/bin/python2
# -*- coding: utf-8 -*-

from django.http import Http404
from django.contrib import messages
from extensions.templates import TemplateHelper
from jinja2 import Environment, PackageLoader
from umfrage.models import Umfrage, Option, Vote
from django.contrib.auth.decorators import login_required

t = TemplateHelper('umfrage')


@login_required
def list(request):
    return t.render('list.djhtml', {'umfragen': Umfrage.objects.all()},
                    req=request)


@login_required
def umfrage(request, umfrage_id):
    try:
        u = Umfrage.objects.get(pk=umfrage_id)
    except Umfrage.DoesNotExist:
        raise Http404

    if request.POST and request.is_ajax():
        reqdata = request.POST

        option_cache = []
        
        for (key, value) in reqdata.iteritems():
            try:
                option_id = int(key)
                
                option = Option.objects.get(pk=option_id)

                if len(Vote.objects.filter(user=request.user,
                       option=option)):
                    response = {'success': False}
                    message.error(request, 'Bereits gevotet für Option'
                                  + option.titel)
                    break

                if (value == -1 and not u.nein) or (value == 0 and not u.vielleicht):
                    response = {'success': False}
                    message.error(request, 'Falsche Optionen ausgewählt')
                    break
                
                response = {'success': True}
                
                option_cache.append((option, value))
            except ValueError:

                pass

        # check the number of votes and so on.
        if len(option_cache) != u.wahlanzahl and u.wahlanzahl != 0:
            response = {'success': False}
            message.error(request, 'Du hast zu viele oder zu wenige Optionen gewählt')
            
        if response['success']:
            for o in option_cache:
            
                vote = Vote()
                vote.option = o[0]
                vote.user = request.user
                vote.umfrage = o[0].umfrage
                vote.choice = o[1]
                vote.save()

        if response['success']:
            messages.success(request, 'Erfolgreich eingetragen')

        return t.ajax(response)
    else:
        if u.typ == 0:
            choices = {-1: '', 0: '', 1: ''}
        else:
            choices = {-1: 'Nein', 0: 'Vielleicht', 1: 'Ja'}
        return t.render('umfrage.djhtml', {
            'umfrage': u,
            'optionen': u.optionen.all(),
            'votes': u.votes.all(),
            'currentuser': request.user,
            'choices': choices,
            }, req=request)
