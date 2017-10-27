# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import bcrypt
from datetime import datetime

class PersonManager(models.Manager):

	def login(self, form_data):
	
		errors = []

		try:

			user = Person.objects.get(email = form_data['email'])
			print user.email
			
			if bcrypt.checkpw(form_data['password'].encode(), user.password.encode()):
				print "in the success user/pass"
				return {'result': 'success', 'user': user}
			
			else:
				errors.append("Invalid password")
				print bcrypt.checkpw(form_data['password'].encode(), user.password.encode())
				print user.password
				print "in the invalid check"
				return {'result': 'fail', 'errors': errors}

		except:
			print "in the email error check"
			errors.append("Invalid credentials")
			return {'result': 'fail', 'errors': errors}


	def register(self, form_data):

		errors=[]

		if len(form_data['name']) < 3:
			errors.append("The name must be at least three characters")
		
		if len(form_data['alias']) < 3:
			errors.append("The alias must be at least three characters")

		if len(form_data['birth']) < 1:
			errors.append("Please enter a birth date")

		if len(form_data['password']) < 8:
			errors.append("The password must be at least eight characters")

		if form_data['password'] != form_data['confirm_password']:
			errors.append("The passwords do not match")

		try:
			user = Person.objects.get(email = form_data['email'])
			errors.append("Email already in use")
		except:
			pass

		if errors:
			print "Registration form errors detected"
			return {'errors':errors}
		else:
			print "No errors in registration form"
			person = Person.objects.create(\
				name = form_data['name'],\
				alias = form_data['alias'],\
				email = form_data['email'],\
				birth = form_data['birth'],\
				password = bcrypt.hashpw(form_data['password'].encode(), bcrypt.gensalt())
				)
			print person.id
			return {'success':person}


class Person(models.Model):
	name			= models.CharField(max_length=100)
	alias			= models.CharField(max_length=100)
	email 			= models.CharField(max_length=100)
	password		= models.CharField(max_length=255)
	birth			= models.DateTimeField(null=True)
	created_at		= models.DateTimeField(auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)
	objects			= PersonManager()




class QuoteManager(models.Manager):

	def add_quote(self, form_data, owner_id):
		
		errors = []

		#no blank entries
		if len(form_data['quoteby']) < 3 \
		or len(form_data['quotation']) < 10:
			print "quote manager validation failed"
			errors.append("Check fields; Quote By must be at least three characters, and Quotation must be at least ten.")
		
		if errors:
			return {'errors':errors}
			return redirect('/quotes')

		else: 
			quote = Quote.objects.create(\
				quoteby = form_data['quoteby'], \
				quotation = form_data['quotation'], \
				owner = Person.objects.get(id = owner_id)
				)
			return {'success':quote}

class Quote(models.Model):
	quoteby			= models.CharField(max_length=55)
	quotation		= models.CharField(max_length=255)
	owner			= models.ForeignKey(Person, related_name="created_quotes")
	favorited		= models.ManyToManyField(Person, related_name="favorited_quotes")
	created_at		= models.DateTimeField(auto_now_add=True)
	updated_at		= models.DateTimeField(auto_now=True)
	objects			= QuoteManager()