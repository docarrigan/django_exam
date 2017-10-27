# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def index(request):
	return render(request, 'quoteapp/index.html')

def logout(request):
	del request.session['id']
	return redirect('/')



def quotes(request):
	
	user 		= Person.objects.get(id=(request.session['id']))
	allquotes 	= Quote.objects.exclude(favorited=request.session['id'])
	favquotes 	= Quote.objects.filter(favorited=request.session['id']).all()
	context = {
		'users': user,
		'allquotes': allquotes,
		'favquotes': favquotes
	}

	return render(request, 'quoteapp/quotes.html', context)


def addquote(request):
	result = Quote.objects.add_quote(request.POST, request.session['id'])

	if 'errors' in result:
		print (result)
		for i in result['errors']:
			messages.error(request, i)
		return redirect('/quotes')

	else:
		print "quote added successfully"
		messages.success(request, "New quote added!")

	return redirect('/quotes')


def favorite(request, quote_id):
	quote = Quote.objects.get(id=quote_id)
	user = Person.objects.get(id=request.session['id'])
	quote.favorited.add(user)
	return redirect('/quotes')


def remove(request, quote_id):
	quote = Quote.objects.get(id=quote_id)
	user = Person.objects.get(id=request.session['id'])
	quote.favorited.remove(user)
	return redirect('/quotes')


def user(request, user_id):
	user = Person.objects.get(id=user_id)
	allquotes 	= Quote.objects.filter(owner=user_id).all()
	count = Quote.objects.filter(owner=user_id).count()

	context = {
		'users': user,
		'allquotes': allquotes,
		'count': count
	}

	return render(request, 'quoteapp/user.html', context)


def register(request):

	result = Person.objects.register(request.POST)
	
	if 'errors' in result:
		print (result)
		for i in result['errors']:
			messages.error(request, i)
		return redirect('/')
	
	else:
		print "New user registered"
		messages.success(request, "You successfully registered. Please log in.")
		return redirect('/')

	return redirect('/')



def login(request):

	login = Person.objects.login(request.POST)

	if login['result'] == 'success':
		request.session['id'] = login['user'].id
		print "User logged in"
		return redirect('/quotes')

	else:
		print "login errors detected"
		for err in login['errors']:
			messages.error(request, err)
		return redirect('/')