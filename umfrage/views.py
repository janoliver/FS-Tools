#!/usr/bin/python2
# -*- coding: utf-8 -*-

from django.http import Http404
from django.contrib import messages
from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import render_to_response
from umfrage.models import Umfrage, Option, Vote
from django.contrib.auth.decorators import login_required

"""
Die Liste der Umfragen.
"""
@login_required
def list(request):
    return render_to_response('umfrage/list.djhtml',
                              {'umfragen': Umfrage.objects.all()},
                              context_instance=RequestContext(request))

"""
Hier wird eine Umfrage angezeigt bzw. ein neues Voting eingetragen.
"""
@login_required
def umfrage(request, umfrage_id):
    try:
        u = Umfrage.objects.get(pk=umfrage_id)
    except Umfrage.DoesNotExist:
        raise Http404

    # Eintragen einer neuen Abstimmung
    if request.POST and request.is_ajax():
        reqdata = request.POST

        option_cache = []

        # hier wird über die Auswahl des Nutzers iteriert.
        # key hat die id der Option, value den Code der Antwort.
        for (key, value) in reqdata.iteritems():
            try:
                option_id = int(key)
                option = Option.objects.get(pk=option_id)

                # Überprüfen, ob bereits eine Antwort auf diese Frage
                # mit dieser Option in der Datenbank existiert.
                if len(Vote.objects.filter(user=request.user,
                       option=option)):
                    response = {'success': False}
                    messages.error(request, 'Bereits gevotet für Option'
                                    + option.titel)
                    break

                # Überprüfe, ob die Antwort erlaubt ist. 
                if value == -1 and not u.nein or value == 0 \
                    and not u.vielleicht:
                    response = {'success': False}
                    messages.error(request,
                                   'Falsche Optionen ausgewählt')
                    break

                # ansonsten success auf true setzen
                response = {'success': True}
                option_cache.append((option, value))
                
            except ValueError:

                pass

        # überprüfe, ob die Anzahl der Auswahl den Vorgaben entspricht
        if len(option_cache) != u.wahlanzahl and u.wahlanzahl != 0:
            response = {'success': False}
            messages.error(request,
                           'Du hast zu viele oder zu wenige Optionen gewählt'
                           )

        # Wenn alles in Ordnung war, dann die Votes in die DB eintragen.
        if response['success']:
            for o in option_cache:

                vote = Vote()
                vote.option = o[0]
                vote.user = request.user
                vote.umfrage = o[0].umfrage
                vote.choice = o[1]
                vote.save()

            messages.success(request, 'Erfolgreich eingetragen')

        # Ergebnis zurückgeben
        return HttpResponse(simplejson.dumps(response),'application/json')
    
    else:
        if u.typ == 0:
            choices = {-1: '', 0: '', 1: ''}
        else:
            choices = {-1: 'Nein', 0: 'Vielleicht', 1: 'Ja'}
        return render_to_response('umfrage/umfrage.djhtml', {
            'umfrage': u,
            'optionen': u.optionen.all(),
            'votes': u.votes.all(),
            'currentuser': request.user,
            'choices': choices,
            },
                                  context_instance=RequestContext(request))
