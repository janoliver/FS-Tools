#!/usr/bin/python2
# -*- coding: utf-8 -*-

from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from ppp.models import PPPUmfrage, Student, Nominierung
from datetime import datetime
from django.template import RequestContext
from django.db import transaction

# Die Liste der Umfragen.
@login_required
def list(request):
    return render_to_response('ppp/list.djhtml',
                              {'umfragen': PPPUmfrage.objects.all()},
                              context_instance=RequestContext(request))

# Details einer Umfrage, sprich, die Liste der Nominierungen
@login_required
def details(request, ppp_id):
    try:
        u = PPPUmfrage.objects.get(pk=ppp_id)
    except PPPUmfrage.DoesNotExist:
        raise Http404

    return render_to_response('ppp/details.djhtml',
                              {'umfrage':u})

@login_required
def matrikelnr_del(request, ppp_id):
    try:
        u = PPPUmfrage.objects.get(pk=ppp_id)
    except PPPUmfrage.DoesNotExist:
        raise Http404

    Student.objects.filter(umfrage=u).delete()
    messages.success(request, "Nummern gelöscht.")
    return HttpResponseRedirect('/ppplist')

    
# Matrikelnummer Eingabe.
@login_required
def matrikelnr(request, ppp_id):
    try:
        u = PPPUmfrage.objects.get(pk=ppp_id)
    except PPPUmfrage.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        reqdata = request.POST
        dat = reqdata['text']
        rows = dat.splitlines()
        err = False

        # we clear the table first
        Student.objects.filter(umfrage=u).delete()

        # and now insert the individual rows
        with transaction.commit_manually():
            for row in rows:
                mnr, gebdat = row.split(',')
                try:
                    gebdat_time = datetime.strptime(gebdat.strip(), '%d.%m.%Y')
                    s = Student()
                    s.umfrage = u
                    s.matrikelnummer = mnr.strip()
                    s.geburtstag = gebdat_time
                    s.save()
                except ValueError:
                    messages.error(request, 'Datum hat falsches Format!')
                    err = True
                    break
            if not err:
                transaction.commit()
                messages.success(request, 'Erfolgreich gespeichert')
            else:
                transaction.rollback()

    return render_to_response('ppp/matr.djhtml',
                              {'umfrage':u},
                              context_instance=RequestContext(request))

# Die Abstimmungsview. Diese ist sichtbar für alle!
def abstimmen(request):
    # finde laufende Umfragen. Sollten es mehrere sein,
    # nimm die erste.
    try:
        u = PPPUmfrage.objects.filter(
            ppp_start__lt=datetime.now()
            ).filter(
            ppp_end__gte=datetime.now()
            )[0]
    except PPPUmfrage.DoesNotExist:
        raise Http404

    data = None
    # abgeschickt
    if request.method == 'POST':
        reqdata = request.POST
        try:
            row = Student.objects.filter(
                matrikelnummer=reqdata['mnr'].strip()
                ).filter(
                geburtstag=datetime.strptime(reqdata['gebdat'], '%d.%m.%Y')
                )[0]
        except (Student.DoesNotExist, ValueError):
            messages.error(request, 'Diese Matrikelnummer konnte nicht gefunden \
                                     werden!')
            data = reqdata
        else:
            # Trage Nominierung nur ein, wenn ein Name angegeben wurde. 
            if reqdata['prof_name'].strip() != '':
                n = Nominierung()
                n.umfrage = u
                n.typ = True
                n.person = reqdata['prof_name'].strip()
                n.text = reqdata['prof_text'].strip()
                n.save()
            if reqdata['nach_name'].strip() != '':
                n = Nominierung()
                n.umfrage = u
                n.typ = False
                n.person = reqdata['nach_name'].strip()
                n.text = reqdata['nach_text'].strip()
                n.save()
            messages.success(request, 'Deine Nominierung wurde \
                                       gespeichert. Vielen Dank!')
            row.delete()

    return render_to_response('ppp/abstimmen.djhtml',
                              {'umfrage':u, 'dat' : data},
                              context_instance=RequestContext(request))
