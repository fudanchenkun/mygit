#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms

class AddForm(forms.Form):
    keywords=forms.CharField()
    sumbox=forms.IntegerField()
    timebox=forms.IntegerField()
    ratebox=forms.IntegerField()

