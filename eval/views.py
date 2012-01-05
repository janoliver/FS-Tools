# -*- coding: utf-8 -*-

#import re, os

from django.http import Http404
from eval.models import Vlu, Vorlesung, Studiengang, Antwortbogen, Personal, Antwort
from fstools.extensions.templates import TemplateHelper
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

t = TemplateHelper('eval')

@login_required
def home(request):
    return t.render('home.djhtml', {
            'vlus': Vlu.objects.all(),
            })

@login_required
def vl(request, vl_id):
    try:
        vl = Vorlesung.objects.get(pk=vl_id)
    except Vorlesung.DoesNotExist:
        raise Http404

    return t.render('vorlesung.djhtml', {
            'vl': vl
            })

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
        
        ab.tutor = Personal.objects.get(pk=reqdata['tutor'])
        ab.studiengang = Studiengang.objects.get(pk=reqdata['studiengang'])
        ab.semester = reqdata['semester']
        ab.vorlesung = vl
        ab.save()
        transaction.commit()
        
        with transaction.commit_on_success():
            for fragenset in fragensets:
                for frage in fragenset.fragen.all():
                    
                    try:
                        antwort = ab.antworten.get(frage=frage)

                        if reqdata['frage' + str(frage.id)] == '' or reqdata['frage' + str(frage.id)] == 0:
                            antwort.delete()
                            continue
                    
                    except Antwort.DoesNotExist:
                        if reqdata['frage' + str(frage.id)] == '' or reqdata['frage' + str(frage.id)] == 0:
                            continue
                        
                        antwort = Antwort()
                    
                        antwort.antwortbogen = ab
                        antwort.frage = frage
                    
                    if frage.fragentyp.texttype:
                        antwort.text = reqdata['frage' + str(frage.id)]
                    else:
                        option = frage.fragentyp.optionen.get(pk=reqdata['frage' + str(frage.id)])
                        antwort.option = option

                    antwort.save()

        messages.success(request, 'Erfolgreich eingetragen')

        if not bogen_id:
            ab = Antwortbogen()
            
    return t.render('editbogen.djhtml', {
            'fragensets': fragensets,
            'vl': vl,
            'ab': ab,
            'studiengaenge': Studiengang.objects.all()
            }, req=request)

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
            for key, val in reqdata.iteritems():
                if key.find('antwort') == 0:
                    a = Antwort.objects.get(pk=int(key[7:]))
                    a.text = val
                    a.save()

        messages.success(request, "Kommentare gespeichert")
    
    textcomments = Antwort.objects.filter(antwortbogen__vorlesung=vl, frage__fragentyp__texttype=True)
    
    return t.render('comments.djhtml', {
            'vl': vl,
            'antworten': textcomments
            }, req=request)
    

# import für die RHP WS 2011
"""    
def filteruml(string):
    if not string:
        return None
    string = string.replace('"u', 'ü')
    string = string.replace('"a', 'ä')
    string = string.replace('"o', 'ö')
    string = string.replace('"U', 'Ü')
    string = string.replace('"O', 'Ö')
    string = string.replace('"A', 'Ä')
    string = string.replace('"s', 'ß')
    string = string.strip()
    if string == 'Verschiedene': string = None
    return string


def imports(request):

    # map
    questionmap = [
        'tutor',
        'studiengang',
        'semester',
        ]

    tutoren = {
        1 : ["Heinz Jänsch", ],
        2 : ["Marcus Assmann", ],
        3 : ["Tillmann", ],
        4 : ["Jung", ],
        5 : ["Beck", ],
        6 : ["Hühn und Bigall", ],
        7 : ["Martin Koch", ],
        8 : ["Wolfgang Heimbrodt", "Prof. Heimbrodt" ],
        9 : ["Florian Gebhard", ],
        10 : ["Alexander Mai",  ],
        11 : ["Daniel Ruhl", ],
        12 : ["Reinhard Noack", "Prof. Noack", "Prof. Dr. R. M. Noack" ],
        13 : ["Jens Güdde", "Jens Güedde" ],
        14 : ["Kristina Klaß", "Kristina Kla\ss", "Kristina Kla�"  ],
        15 : ["Ulrich Höfer", ],
        16 : ["Peter Jakob", ],
        17 : ["Gregor Witte", ],
        18 : ["Bruno Eckhardt", ],
        19 : ["Tobias Madré", "Tobias Madre", ],
        20 : ["Stephan Koch", ],
        21 : ["Christoph Böttge", ],
        22 : ["Benjamin Breddermann", ],
        23 : ["Jens Pfeiffer", ],
        24 : ["Wolfgang Einhäuser-Treyer", ],
        25 : ["Lukas Schneebeli", ],
        26 : ["Wolfgang Parak", ],
        27 : ["Nadja Bigall", ],
        28 : ["Peter Lenz", ],
        29 : ["Sangam Chatterjee", ],
        30 : ["Kolja Kolata", ],
        31 : ["Andreas Schrimpf", ],
        32 : ["Volz, Klingl, Gries", ],
        33 : ["Gries", ],
        34 : ["Sergei Baranovski", ],
        35 : ["Peter Thomas", ],
        36 : ["Mootz", ],
        37 : ["Stefan Busch", ],
        38 : ["Reuter", ],
        39 : ["Michael Grau", ]
        }
    
    studg = {
        1 : ["Bachelor Physik", "Bachlor Physik", "B.\,Sc. Physik", "B.\,Sc. Physik mit Schwerpunkt Informatik", "B.\,Sc. Physik allgemein", "Physik BA",
             "B.\,Sc. Physik mit Schwerpunkt Biologie", "Physik Bachelor"],
        2 : ["Master Physik", "MasterPhysik", "M.\,Sc.", "M.\,Sc. Physik" ],
        3 : ["Diplomphysik", "Diplom Physik", ],
        4 : ["Master Chemie", "M.\,Sc. Chemie"],
        5 : ["Lehramt Physik", ],
        6 : ["Bachelor Biologie", "B.\,Sc. Biologie"],
        7 : ["Promotion Pharmazie"],
        8 : ["Bachelor Humanbiologie", "Humanbiologe", "Humanbiolage"],
        9 : ["Bachelor Mathematik", "Mathe Bachelor"],
        10: ["Bachelor BWL"],
        11: ["Bachelor Geographie"],
        12: ["Diplominformatik", "Diplom Informatik"],
        13: ["Bachelor Chemie", "B.\,Sc. Chemie", "B.\,Sc.Chemie"]
        }
    
    vls = {
        14: "Single-particle properties of solids.dbf",
        3 : "Klassische Feldtheorie und statistische Physik.dbf",
        1 : "Mechanik.dbf",
        20: "Electron microscopy in biology and materials sience.dbf",
        9 : "Computational physics I.dbf",
        11: "Nonlinear dynamics.dbf",
        4 : "Feldtheorie und Thermodynamik.dbf",
        8 : "Molecular materials and electronic devices.dbf",
        18: "Einfuehrung in die Astronomie.dbf",
        2 : "Optik und Quantenphaenomene.dbf",
        15: "Physik I fuer Zahnmediziner, Humanbiologen und Pharmazeuten.dbf",
        12: "Magnetism of ions.dbf",
        21: "Mathevorkurs.dbf",
        19: "Experimentalphysik fuer Naturwissenschaftler.dbf",
        16: "Theory of general relativity.dbf",
        6 : "Halbleiterphysik und Halbleiterbauelemente.dbf",
        10: "Quantenmechanik II.dbf",
        7 : "Oberflachenphysik.dbf",
        17: "Moderne Themen der Schulphysik.dbf",
        22: "MathemErg.dbf",
        5 : "Festkoerperphysik.dbf",
        }

    vlu = Vlu.objects.get(pk=1)
    print "VLU:", vlu
    
    for filee in os.listdir('../../WS2011/server'):
        
        if filee.find('.dbf') > -1:
            count = 0
            for line in open('../../WS2011/server/' + filee, 'r'):
                
                questions = line.split(chr(0))
                
                if len(questions) != 37:
                    continue
                
                count += 1
                
                bogen = dict()
                
                for qkey,x in enumerate(questions):
                
                    a = re.findall(r'[^'+chr(1)+chr(2)+chr(3)+']+', x)
                
                    if len(a) < 2:
                        a.append(None)

                    # insert values into bogen dict
                    if qkey > 2:
                        bogen[qkey-1] = filteruml(a[1])
                    else:
                        bogen[questionmap[qkey]] = filteruml(a[1])

                # finde tutor id
                tutor = None
                for k,te in tutoren.iteritems():
                    if bogen['tutor'] and (bogen['tutor'] in te or " ".join(te).find(bogen['tutor']) > -1):
                        tutor = k
                if not tutor and bogen['tutor']:
                    print "Tutor not found: ", filee, bogen['tutor']
                    exit()

                # finde studg id
                studiengang = None
                for k,te in studg.iteritems():
                    if bogen['studiengang'] and (bogen['studiengang'] in te or " ".join(te).find(bogen['studiengang']) > -1):
                        studiengang = k
                if not studiengang and bogen['studiengang']:
                    print "Studiengang not found: ", filee, bogen['studiengang']
                    exit()

                # baue antwortbogen objekt zusammen
                ab = Antwortbogen()
                vlid = [k for k, v in vls.iteritems() if v == filee][0]
                vl = Vorlesung.objects.get(pk=vlid)
                if studiengang: ab.studiengang = Studiengang.objects.get(pk=studiengang)
                if tutor: ab.tutor = Personal.objects.get(pk=tutor)
                ab.semester = bogen['semester']
                ab.vorlesung = vl
                ab.user = request.user
                ab.save()

                for fragenset in vl.fragebogen.fragensets.all():
                    for frage in fragenset.fragen.all():

                        if not bogen[frage.id] or bogen[frage.id] == '0':
                            continue
                        
                        antwort = Antwort()
                        antwort.antwortbogen = ab
                        antwort.frage = frage
                        
                        if frage.fragentyp.texttype:
                            antwort.text = bogen[frage.id]
                        else:
                            option = frage.fragentyp.optionen.all()[int(bogen[frage.id])-1]
                            antwort.option = option
                        antwort.save()

            
    return t.render('home.djhtml', {
            'vlus': Vlu.objects.all(),
            })
"""
