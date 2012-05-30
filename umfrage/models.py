#!/usr/bin/python2
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
import fstools.extensions.models as cmodels


class Umfrage(cmodels.Timestamped_Model):

    UMFRAGETYPEN = ((0, 'Standard'), (1, 'Termin'))

    name = models.CharField(max_length=255)
    typ = models.IntegerField(choices=UMFRAGETYPEN)
    beschreibung = models.TextField(null=True, blank=True)
    wahlanzahl = models.PositiveIntegerField(default=1,
            help_text='Anzahl der Wahlmöglichkeiten. 0 = unbegrenzt')
    vielleicht = models.BooleanField(default=False,
            help_text = 'Soll es die Option "Vielleicht" geben?')
    nein = models.BooleanField(default=True,
            help_text = 'Soll es die Option "Nein" geben?')
    anonym = models.BooleanField(default=False,
            help_text = 'Anonyme Umfrage?')
    mindest_wahl = models.BooleanField(default=True,
            help_text = 'Müssen alle unter "Wahlanzahl" angegebenen Optionen genutzt werden?')
    unbeeinflusst = models.BooleanField(default=True,
            help_text = 'Sollen Ergebnisse erst angezeigt werden, nachdem der Benutzer abgestimmt hat?')
    
    def getUser(self):
        ar = dict()
        for v in self.votes.select_related():
            if not v.user in ar:
                ar[v.user] = dict()
            ar[v.user][v.option] = v

        return ar


    class Meta:

        verbose_name_plural = 'Umfragen'


    def __unicode__(self):
        return self.name


class Option(cmodels.Timestamped_Model):

    titel = models.CharField(max_length=255)
    rank = models.PositiveIntegerField()
    umfrage = models.ForeignKey('Umfrage', related_name='optionen')


    class Meta:

        verbose_name_plural = 'Optionen'
        ordering = ['rank']


    def __unicode__(self):
        return self.titel


class Vote(cmodels.Timestamped_Model):

    user = models.ForeignKey(User, related_name='votes')
    option = models.ForeignKey('Option', related_name='votes')
    umfrage = models.ForeignKey('Umfrage', related_name='votes')
    choice = models.IntegerField(null=True)

    def __unicode__(self):
        return "Option"


