# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from ..login.models import User

# Create your models here.
class TripManager(models.Manager):
    def add(self, data, username):
        results = {'status': True, 'errors': []}
        if not data['destination'] or len(data['destination']) < 3:
            results['errors'].append("'Destination' must be at least 3 characters")
            results['status']= False
        if not data['description'] or len(data['description']) < 3:
            results['errors'].append("'Description' must be at least 3 characters")
            results['status'] = False
        if not data['travel_from']:
            results['errors'].append("'Travel Date From' can not be blank")
            results['status'] = False     
        if not data['travel_to']:
            results['errors'].append("'Travel Date To' can not be blank")
            results['status'] = False 
        if data['travel_from']:
            fyear, fmonth, fday= map(int, data['travel_from'].split('-'))
            fdate =  datetime.date(fyear, fmonth, fday)
            if datetime.date.today() > fdate:
                results['errors'].append("'Travel From Date' must be in the future")
                results['status'] = False
        if data['travel_to'] and data['travel_from']:
            tyear, tmonth, tday= map(int, data['travel_to'].split('-'))
            tdate =  datetime.date(tyear, tmonth, tday)
            if fdate > tdate:
                results['errors'].append("'Travel To Date' must be later than 'Travel From Date'")
                results['status'] = False
        if results['status']:
            creator = User.objects.get(username=username)
            Trip.objects.create(
                destination=data['destination'], 
            description=data['description'], 
            creator=creator,
            date_from=fdate,
            date_to = tdate
            )
        return results
    def join(self, id, username):
        trip = Trip.objects.get(id=id)
        user = User.objects.get(username=username)
        trip.joiners.add(user)
        trip.save()

class Trip(models.Model):
    destination = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    creator = models.ForeignKey('login.User')
    joiners = models.ManyToManyField('login.User', related_name="joined")
    date_from = models.DateField()
    date_to = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()