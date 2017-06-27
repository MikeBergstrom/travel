# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import datetime


def index(request):
    # User.objects.all().delete()
    return render(request, 'login/index.html')

def login(request):
    print "in login view"
    user= User.objects.login(request.POST)
    if user['status']:
        print "in login view success"
        request.session['name'] = user['user'].name
        request.session['username'] = user['user'].username
        #Insert starting page in redirect below
        return redirect ('trips:index')
    else:
        print "login view returned errors"
        for error in user['errors']:
            messages.error(request, error, extra_tags="login")
        return redirect('auth:index')

def register(request):
    print "in register"
    user = User.objects.register(request.POST)
    print user
    if not user['status']:
        for error in user['errors']:
            messages.error(request, error, extra_tags="register")
        return redirect ('auth:index')
    else:
        print "register success"
        print user['user'].name
        request.session['name'] = user['user'].name
        request.session['username'] = user['user'].username
        print request.session['name']
        #Insert starting page in redirect below
        return redirect ('trips:index')    

def logout(request):
    request.session.pop('name')
    return redirect('auth:index')