from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from fstools.extensions.templates import TemplateHelper, LatexHelper
from jinja2 import Environment,  PackageLoader
from rhp.models import Rhp, Artikel
from eval.models import Vlu, Frage, Fragenset, Option
from django.contrib.auth.decorators import login_required
import os, shutil

t = TemplateHelper('rhp')

@login_required
def list(request):
    return t.render('list.djhtml', {'rhps': Rhp.objects.all(),}, req=request)

@login_required
def artikel(request, rhp_id, artikel_id=None):
    try:
        rhp = Rhp.objects.get(pk=rhp_id)
    except Rhp.DoesNotExist:
        raise Http404

    # check if a sheet is to be edited
    print artikel_id
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
        artikel.text  = reqdata['text']
        artikel.save()
        messages.success(request, 'Erfolgreich gespeichert')
    
    return t.render('artikel.djhtml', {
            'artikel': artikel,
            'rhp': rhp
            }, req=request)

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
    return HttpResponseRedirect("/rhp")

@login_required
def export(request, rhp_id):
    try:
        rhp = Rhp.objects.get(pk=rhp_id)
    except Rhp.DoesNotExist:
        raise Http404

    # create the jinja2 evironment for latex response
    #loader = FileSystemLoader('/path/to/templates')
    loader = PackageLoader('rhp', 'templates/latex')
    latex_helper = LatexHelper(loader)

    context = {
        'rhp': rhp,
        'vlu': rhp.vlu,
        'fragen': Frage.objects.select_related(),
        'fragensets': Fragenset.objects.select_related(),
        'optionen': Option.objects.select_related(),
        'vorlesungen': rhp.vlu.vorlesungen.select_related(),
        'artikel': rhp.artikel.all()
        }
        
    for tpl in latex_helper.env.list_templates():
        if tpl and (tpl.find('.tex') > 0 or tpl.find('.sty') > 0):
            template = latex_helper.env.get_template(tpl)
            f = open(rhp.saveto + tpl, 'w')
            f.write(template.render(context).encode("utf8"))
            f.close()
        else:
            shutil.copy(loader.get_source(latex_helper.env, tpl)[1], rhp.saveto)
            
    messages.success(request, 'Erfolgreich erstellt.')
    return HttpResponseRedirect("/rhp")