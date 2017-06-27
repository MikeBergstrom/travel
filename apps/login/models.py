# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import datetime
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile('^[a-zA-Z]+$')



class UserManager(models.Manager):
    def register(self, data):
        results = {'status':True, 'errors':[], 'user':None}
        print "model register"
        # print data['first']
        # month, day, year = map(int, data['birth'].split('/'))
        # print datetime.date.today()
        # print datetime.date(year, month, day)
        if not data['name'] or len(data['name']) < 3:
            results['errors'].append('Name must be at least 3 characters')
            results['status']= False
        if not data['username'] or len(data['username']) < 3:
            results['errors'].append('Username must be at least 3 characters')
            results['status'] = False
        # if not NAME_REGEX.match(data['first']):
        #     results['errors'].append('First name must be letters only')
        #     results['status'] = False
        # if not NAME_REGEX.match(data['last']):
        #     results['errors'].append('Last name must be letters only')
        #     results['status'] = False
        # if datetime.date(year, month, day) >= datetime.date.today():
        #     errors.append('Birth date must be in the past')
        #     pass
        if data['password'] != data['confirm']:
            results['errors'].append('Passwords do not match')
            results['status'] = False
        if len(data['password']) < 8:
            results['errors'].append('Password must be at least 8 characters')
            results['status'] = False
        if User.objects.filter(username=data['username']).exists():
            results['errors'].append('This username is already in use, please choose another')
            results['status'] = False
        if results['status']:
            password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
            print "successful register"
            user = User.objects.create(name=data['name'], username=data['username'], password=password)
            results['user'] = user
            print results
        return results


    def login(self, data):
        results = {'status': True, 'errors':[], 'user': None}
        if not User.objects.filter(username=data['username']).exists():
            results['errors'].append('Email or Password is not correct')
            results['status'] = False
        else:
            user = User.objects.get(username=data['username'])
            passhash = bcrypt.hashpw(data['password'].encode(), user.password.encode())
            if not passhash == user.password.encode():
                print "bad password"
                results['errors'].append('Email or Password is not correct')
                results['status']= False
            else:
                results['user'] = user
                print user
        return results

    def update(self, data):
        user = User.objects.get(id=data['id'])
        user.email = data['email']
        user.first_name = data['first']
        user.last_name = data['last']
        user.save()
        return user

class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    objects = UserManager()
