#!/usr/bin/python2
# -*- coding: utf-8 -*-
from django.http import Http404

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from jinja2 import PackageLoader
from rhp.models import Rhp, Artikel
from eval.models import Vlu, Frage, Fragenset, Option
from django.contrib.auth.decorators import login_required
import zipfile
import tempfile
from cStringIO import StringIO
from django.shortcuts import render_to_response
from fstools.extensions.templates import LatexHelper

@login_required
def list(request):
    return render_to_response('rhp/list.djhtml', {'rhps': Rhp.objects.all()},
                              context_instance=RequestContext(request))


@login_required
def artikel(request, rhp_id, artikel_id=None):
    try:
        rhp = Rhp.objects.get(pk=rhp_id)
    except Rhp.DoesNotExist:
        raise Http404

    # check if a sheet is to be edited

    if artikel_id:
        try:
            artikel = Artikel.objects.get(pk=artikel_id)
        except Artikel.DoesNotExist:
            raise Http404
    else:
        artikel = Artikel()

    if request.method == 'POST':
        reqdata = request.POST
        artikel.rhp = rhp
        artikel.autor = reqdata['autor']
        artikel.titel = reqdata['titel']
        artikel.text = reqdata['text']
        artikel.save()
        messages.success(request, 'Erfolgreich gespeichert')

    return render_to_response('rhp/artikel.djhtml', {'artikel': artikel, 'rhp': rhp},
                              context_instance=RequestContext(request))


@login_required
def move(request, direction, artikel_id):
    try:
        artikel = Artikel.objects.get(pk=artikel_id)
    except Artikel.DoesNotExist:
        raise Http404

    if artikel.rank > 0 and direction == 'up':
        artikel.rank -= 1

    if direction == 'down':
        artikel.rank += 1

    artikel.save()
    messages.success(request, 'Erfolgreich bewegt')
    return HttpResponseRedirect('/rhp')


@login_required
def export(request, rhp_id):
    try:
        rhp = Rhp.objects.get(pk=rhp_id)
    except Rhp.DoesNotExist:
        raise Http404

    # create the jinja2 evironment for latex response
    # loader = FileSystemLoader('/path/to/templates')

    loader = PackageLoader('rhp', 'templates/latex')
    latex_helper = LatexHelper(loader)

    context = {
        'rhp': rhp,
        'vlu': rhp.vlu,
        'fragen': Frage.objects.select_related(),
        'fragensets': Fragenset.objects.select_related(),
        'optionen': Option.objects.select_related(),
        'vorlesungen': rhp.vlu.vorlesungen.select_related(),
        'artikel': rhp.artikel.all(),
        }

    files = []
    tmpfiles = []
    for tpl in latex_helper.env.list_templates():
        if tpl and (tpl.find('.tex') > 0 or tpl.find('.sty') > 0):
            template = latex_helper.env.get_template(tpl)
            f = tempfile.NamedTemporaryFile()
            f.write(template.render(context).encode('utf8'))
            f.flush()
            tmpfiles.append((tpl, f))
        else:
            files.append((tpl, loader.get_source(latex_helper.env,
                         tpl)[1]))

    # return as a zip file. from here: https://code.djangoproject.com/wiki/CookBookDynamicZip

    response = HttpResponse(mimetype='application/zip')
    response['Content-Disposition'] = 'filename=' + rhp.name + '.zip'

    buffer = StringIO()
    zip = zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED)

    for (name, f) in tmpfiles:
        zip.write(f.name, rhp.name + '/' + name)
        f.close()

    for (name, f) in files:
        zip.write(f, rhp.name + '/' + name)

    zip.close()
    buffer.flush()

    response.write(buffer.getvalue())
    buffer.close()
    return response
