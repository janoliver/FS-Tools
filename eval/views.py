#!/usr/bin/python2
# -*- coding: utf-8 -*-

from django.http import Http404, HttpResponse
from eval.models import *
from django.shortcuts import redirect
from extensions.templates import LatexHelper
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
import zipfile
import tempfile
from cStringIO import StringIO

# Die Startseite der Eval App (Vorlesungsumfrage)
@login_required
def home(request):
    return render_to_response('eval/home.djhtml', {
            'vlus': Vlu.objects.all(),
            'boegen': Fragebogen.objects.all()})


# Die Einverständniserklärungen-Seite
@login_required
def einverst(request, vl_id):
    try:
        vl = Vorlesung.objects.get(pk=vl_id)
    except Vorlesung.DoesNotExist:
        raise Http404

    return render_to_response('eval/einverst.djhtml', {'vl': vl})


# Diese View setzt die Einverständniserklärung für eine VLU
# auf AN bzw. AUS. Danach wird umgeleitet zur Übersichtsseite
# der Einverständniserklärungen.
@login_required
def einverst_single(request, typ, vl_id, person_id):
    # finde Vorlesung
    try:
        vl = Vorlesung.objects.get(pk=vl_id)
    except Vorlesung.DoesNotExist:
        raise Http404

    # Finde Dozenten/Tutor
    try:
        person = Personal.objects.get(pk=person_id)
    except Vorlesung.DoesNotExist:
        raise Http404

    if typ == 'Dozent':
        conn = VorlesungDozenten.objects.get(vorlesung=vl, dozent=person)
    if typ == 'Tutor':
        conn = VorlesungTutoren.objects.get(vorlesung=vl, tutor=person)

    # toggle Einverstanden
    conn.einverstanden = not conn.einverstanden
    conn.save()
    
    return redirect('/eval/einverst/' + str(vl.id))


# Diese View setzt die Einverständniserklärung für ALLE VLU
# auf AN bzw. AUS. Danach wird umgeleitet zur Übersichtsseite
# der Einverständniserklärungen.
@login_required
def einverst_forever(request, vl_id, person_id):
    # Finde Vorlesung
    try:
        vl = Vorlesung.objects.get(pk=vl_id)
    except Vorlesung.DoesNotExist:
        raise Http404

    # Finde Dozenten/Tutor
    try:
        person = Personal.objects.get(pk=person_id)
    except Vorlesung.DoesNotExist:
        raise Http404

    # Toggle einverstanden
    person.einverst = not person.einverst
    person.save()
    
    return redirect('/eval/einverst/' + str(vl.id))


# Zeige Details einer Vorlesung an.
@login_required
def vl(request, vl_id):
    # Vorlesung finden.
    try:
        vl = Vorlesung.objects.get(pk=vl_id)
    except Vorlesung.DoesNotExist:
        raise Http404

    return render_to_response('eval/vorlesung.djhtml', {'vl': vl})


# 
@login_required
def editbogen(request, vl_id, bogen_id=None):
    try:
        vl = Vorlesung.objects.get(pk=vl_id)
    except Vorlesung.DoesNotExist:
        raise Http404

    # check if a sheet is to be edited

    if bogen_id:
        try:
            ab = Antwortbogen.objects.get(pk=bogen_id)
        except Antwortbogen.DoesNotExist:
            raise Http404
    else:
        ab = Antwortbogen()

    fragensets = vl.fragebogen.fragensets.all()

    if request.method == 'POST':

        # insert bogen into database

        reqdata = request.POST

        if reqdata['tutor'] != '':
            ab.tutor = Personal.objects.get(pk=reqdata['tutor'])

        if reqdata['studiengang'] != '':
            ab.studiengang = \
                Studiengang.objects.get(pk=reqdata['studiengang'])

        if reqdata['semester'] != '':
            ab.semester = reqdata['semester']

        ab.vorlesung = vl
        ab.save()

        # transaction.commit()

        with transaction.commit_on_success():
            for fragenset in fragensets:
                for frage in fragenset.fragen.all():

                    try:
                        antwort = ab.antworten.get(frage=frage)

                        if 'frage' + str(frage.id) not in reqdata \
                            or reqdata['frage' + str(frage.id)] == '' \
                            or reqdata['frage' + str(frage.id)] == 0:
                            antwort.delete()
                            continue
                    except Antwort.DoesNotExist:

                        if 'frage' + str(frage.id) not in reqdata \
                            or reqdata['frage' + str(frage.id)] == '' \
                            or reqdata['frage' + str(frage.id)] == 0:
                            continue

                        antwort = Antwort()

                        antwort.antwortbogen = ab
                        antwort.frage = frage

                    if frage.fragentyp.texttype:
                        antwort.text = reqdata['frage' + str(frage.id)]
                    else:
                        option = \
                            frage.fragentyp.optionen.get(pk=reqdata['frage'
                                 + str(frage.id)])
                        antwort.option = option

                    antwort.save()

        messages.success(request, 'Erfolgreich eingetragen')

        if not bogen_id:
            ab = Antwortbogen()

    return render_to_response('eval/editbogen.djhtml', {
        'fragensets': fragensets,
        'vl': vl,
        'ab': ab,
        'studiengaenge': Studiengang.objects.all(),
        })


@login_required
def comments(request, vl_id):
    try:
        vl = Vorlesung.objects.get(pk=vl_id)
    except Vorlesung.DoesNotExist:
        raise Http404

    if request.method == 'POST':

        # edit comments

        reqdata = request.POST

        with transaction.commit_on_success():
            for (key, val) in reqdata.iteritems():
                if key.find('antwort') == 0:
                    a = Antwort.objects.get(pk=int(key[7:]))

                    # delete the answer if text is empty.

                    if val == '':
                        a.delete()
                    else:
                        a.text = val
                        a.save()

        messages.success(request, 'Kommentare gespeichert')

    textcomments = Antwort.objects.filter(antwortbogen__vorlesung=vl,
            frage__fragentyp__texttype=True)

    return render_to_response('eval/comments.djhtml', {
            'vl': vl,
            'antworten': textcomments
            })


@login_required
def export_einverst(request, vlu_id):
    try:
        vlu = Vlu.objects.get(pk=vlu_id)
    except Vlu.DoesNotExist:
        raise Http404

    # create the jinja2 evironment for latex response
    # loader = FileSystemLoader('/path/to/templates')

    loader = PackageLoader('eval', 'templates/latex')
    latex_helper = LatexHelper(loader)

    context = {
        'vlu': vlu,
        'fragen': Frage.objects.select_related(),
        'fragensets': Fragenset.objects.select_related(),
        'optionen': Option.objects.select_related(),
        'vorlesungen': vlu.vorlesungen.select_related(),
        }

    # return as a zip file. from here:
    # https://code.djangoproject.com/wiki/CookBookDynamicZip

    response = HttpResponse(mimetype='application/zip')
    response['Content-Disposition'] = 'filename=' + vlu.name + '.zip'

    buffer = StringIO()
    zip = zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED)

    for tpl in latex_helper.env.list_templates():
        if tpl and (tpl.find('.tex') > 0 or tpl.find('.sty') > 0):
            template = latex_helper.env.get_template(tpl)
            f = tempfile.NamedTemporaryFile()
            f.write(template.render(context).encode('utf8'))
            f.flush()
            zip.write(f.name, vlu.name + '/' + tpl)
            f.close()

    zip.close()
    buffer.flush()

    response.write(buffer.getvalue())
    buffer.close()
    return response
