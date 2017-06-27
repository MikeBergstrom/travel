# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import Trip
from ..login.models import User
from django.contrib import messages

# Create your views here.
def index(request):
    trips = Trip.objects.all().order_by('date_from')
    user = User.objects.get(username=request.session['username'])
    context = {'trips':trips, 'user':user}
    return render(request, 'trips/index.html', context)

def create(request):
    if request.method == "GET":
        return render(request, 'trips/add.html')
    elif request.method == "POST":
        trip = Trip.objects.add(request.POST, request.session['username'])
        if trip['status'] == False:
            for error in trip['errors']:
                messages.error(request, error)
            return redirect('trips:create')
        return redirect('trips:index')

def join(request, id):
    trip = Trip.objects.join(id, request.session['username'])
    return redirect('trips:index')

def show(request, id):
    trip = Trip.objects.get(id=id)
    trip_joiners = User.objects.filter(joined__id=id)
    context = {'trip':trip, 'trip_joiners':trip_joiners}
    return render(request, 'trips/show.html', context)