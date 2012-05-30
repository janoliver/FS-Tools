#!/usr/bin/python2
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
import fstools.extensions.models as cmodels
from eval.models import Vlu


class Rhp(cmodels.Timestamped_Model):

    name = models.CharField(max_length=255)
    vlu = models.ForeignKey(Vlu, related_name='rhps')
    vorwort = models.TextField()
    saveto = models.CharField(max_length=255,
                              default='/home/fsphysik/rhp/')


    class Meta:

        verbose_name_plural = 'RHP Ausgaben'


    def save(self):
        if self.saveto[-1] != '/':
            self.saveto += '/'
        super(Rhp, self).save()

    def __unicode__(self):
        return self.name


class Artikel(cmodels.Timestamped_Model):

    titel = models.CharField(max_length=255)
    autor = models.CharField(max_length=255)
    rank = models.PositiveIntegerField(blank=True, null=True)
    rhp = models.ForeignKey('Rhp', related_name='artikel')
    text = models.TextField()
    user = models.ForeignKey(User, blank=True, null=True,
                             related_name='artikel')


    class Meta:

        verbose_name_plural = 'Artikel'
        ordering = ['rank']


    def __unicode__(self):
        return self.titel


