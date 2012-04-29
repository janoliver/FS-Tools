# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import extensions.models as cmodels
from django.db.models import Count
from datetime import datetime

class Personal(cmodels.Timestamped_Model):
    personaltyp  = models.ForeignKey('Personaltyp', blank=True, null=True, on_delete=models.SET_NULL)
    titel        = models.CharField(max_length=255, blank=True, null=True)
    name         = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Personal"
    
    def __unicode__(self):
        return self.name

class Vorlesung(cmodels.Timestamped_Model):
    name         = models.CharField(max_length=255)
    vlu          = models.ForeignKey('Vlu', related_name='vorlesungen')
    fragebogen   = models.ForeignKey('Fragebogen', related_name='vorlesungen')
    dozenten     = models.ManyToManyField('Personal', related_name='vorlesungen')
    tutoren      = models.ManyToManyField('Personal', related_name='vorlesungen_tutor', blank=True, null=True)

    antworten_cache = None

    def semester_dist(self):
        return [{'key':x['semester'],'val':x['id__count']} for x in Antwortbogen.objects
                .filter(vorlesung=self,semester__isnull=False)
                .values('semester').annotate(Count('id')).distinct()]
    
    def studiengang_dist(self):
        return [{'key':x['studiengang__name'],'val':x['id__count']} for x in Antwortbogen.objects
                .filter(vorlesung=self,studiengang__isnull=False)
                .values('studiengang__name').annotate(Count('id')).distinct()]

    
    def antworten(self):
        if not self.antworten_cache:
            self.antworten_cache = Antwort.objects.select_related('frage','option').filter(antwortbogen__vorlesung=self)
        return self.antworten_cache

    class Meta:
        verbose_name_plural = "Vorlesungen"
    
    def __unicode__(self):
        return self.name

class Antwortbogen(cmodels.Timestamped_Model):
    semester     = models.IntegerField(blank=True, null=True)
    vorlesung    = models.ForeignKey('Vorlesung', related_name='antwortboegen')
    studiengang  = models.ForeignKey('Studiengang', blank=True, null=True, on_delete=models.SET_NULL)
    tutor        = models.ForeignKey('Personal', related_name='antwortboegen_tutor', blank=True, null=True, on_delete=models.SET_NULL)
    user         = models.ForeignKey(User, blank=True, null=True, related_name='boegen')
    
    def getAntwort(self, fr):
        try:
            antwort  = self.antworten.get(frage=fr)
            if fr.fragentyp.texttype:
                return antwort.text
            else:
                return antwort.option.id
            
        except Antwort.DoesNotExist:
            return ""

    class Meta:
        verbose_name_plural = "Antwortbögen"
        
    def __unicode__(self):
        return 'Bogen: ' + self.vorlesung.name

class Frage(cmodels.Timestamped_Model):
    text         = models.CharField(max_length=255)
    fragentyp    = models.ForeignKey('Fragentyp', null=True, on_delete=models.SET_NULL)

    fragenset_cache = None

    def antworten(self, vl, tutor=None):
        if not tutor:
            return Antwort.objects.filter(frage=self, antwortbogen__vorlesung=vl)
        else:
            return Antwort.objects.filter(frage=self, antwortbogen__vorlesung=vl, antwortbogen__tutor=tutor)

    def belongs_to_fragenset(self, fragenset):
        if not self.fragenset_cache:
            self.fragenset_cache = [x for x in self.fragensets.all()]
        for fs in self.fragenset_cache:
            if fs == fragenset:
                return True
        return False

    def total(self, rel):
        return len([x for x in rel.antworten() if x.frage_id == self.id])
    
    def mean(self, rel):
        # mean of the answers of this question, in relation to rel
        antworten = [x for x in rel.antworten() if x.frage_id == self.id]

        summe = 0.
        for a in antworten:
            summe += a.option.rank

        if summe == 0:
            return 0

        return summe/len(antworten)
    
    class Meta:
        verbose_name_plural = "Fragen"
    
    def __unicode__(self):
        return self.text

class Fragebogen(cmodels.Timestamped_Model):
    name         = models.CharField(max_length=255)
    fragensets   = models.ManyToManyField('Fragenset',through='FragensetFragebogen', related_name='frageboegen')

    class Meta:
        verbose_name_plural = "Fragebögen"
    
    def __unicode__(self):
        return self.name

class FrageFragenset(models.Model):
    frage        = models.ForeignKey('Frage')
    fragenset    = models.ForeignKey('Fragenset')
    rank         = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['rank']
    
class Fragenset(cmodels.Timestamped_Model):
    name         = models.CharField(max_length=255)
    titel        = models.CharField(max_length=255)
    fragen       = models.ManyToManyField('Frage', related_name='fragensets', through='FrageFragenset')
    
    def fragenn(self, fragen):
        return [x for x in fragen if x.belongs_to_fragenset(self)]
    
    class Meta:
        verbose_name_plural = "Fragensets"
    
    def __unicode__(self):
        return self.name

class FragensetFragebogen(models.Model):
    fragenset    = models.ForeignKey('Fragenset')
    fragebogen   = models.ForeignKey('Fragebogen')
    rank         = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['rank']
    
class Vlu(cmodels.Timestamped_Model):
    name         = models.CharField(max_length=255)
    vlu_start    = models.DateTimeField(default=datetime.now)
    vlu_end      = models.DateTimeField(default=datetime.now)

    antworten_cache = None
    
    def antworten(self):
        if not self.antworten_cache:
            self.antworten_cache = Antwort.objects.select_related('frage','option').filter(antwortbogen__vorlesung__vlu=self)
        return self.antworten_cache
    
    class Meta:
        verbose_name_plural = "Vorlesungsumfragen"
    
    def __unicode__(self):
        return self.name


class Fragentyp(cmodels.Timestamped_Model):
    name         = models.CharField(max_length=255)
    texttype     = models.BooleanField()

    def fast_optionen(self, optionen):
        return [x for x in optionen if x.fragentyp == self]
    
    class Meta:
        verbose_name_plural = "Fragentypen"
    
    def __unicode__(self):
        return self.name

class Option(cmodels.Timestamped_Model):
    fragentyp    = models.ForeignKey('Fragentyp', related_name='optionen')
    rank         = models.PositiveIntegerField(blank=True, null=True)
    text         = models.CharField(max_length=255, blank=True)

    def value(self, vl, frage):
        # return the number of choices for this option
        # normed on an interval [0,1]
        antworten = frage.total(vl)
        antworten_opt = len([x for x in vl.antworten() if x.option_id == self.id and x.frage_id == frage.id])
        
        if antworten == 0:
            return 0
        
        return antworten_opt/float(antworten)
    
    class Meta:
        verbose_name_plural = "Antwortoptionen"
        ordering = ['rank']
        
    def __unicode__(self):
        return self.text

class Personaltyp(cmodels.Timestamped_Model):
    name         = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Personaltypen"
    
    def __unicode__(self):
        return self.name

class Studiengang(cmodels.Timestamped_Model):
    name         = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Studiengänge"
    
    def __unicode__(self):
        return self.name

class Antwort(cmodels.Timestamped_Model):
    frage        = models.ForeignKey('Frage')
    option       = models.ForeignKey('Option', null=True)
    text         = models.TextField()
    antwortbogen = models.ForeignKey('Antwortbogen', related_name='antworten')

    class Meta:
        verbose_name_plural = "Antworten"
    
    def __unicode__(self):
        return 'Antwort auf: ' + self.frage.text
