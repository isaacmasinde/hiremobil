from django.shortcuts import render,redirect
from .models import *
from django.http import *
from django.db.models import *
from django.contrib.auth.models import *
from django.contrib.auth import *
from hiremobiluser.views import *
import requests
import json
import random
from django.utils import timezone
from datetime import date 
def index(request):
	types=Car.objects.all()
	for x in types:
		if x.Available==False:
			try:
				deal=Deal.objects.filter(Car=x).last()
				if deal.To < date.today():
					x.Available=True
					x.save()
			except:
				pass
	cars_list=Car.objects.filter(Available=True).order_by('Fee')[:12]
	pickup=	PickLoc.objects.all()
	templatename='index/index.html'
	context={'cars_list':cars_list,'pickup':pickup,'types':types,}
	return render(request,templatename, context)
def detail(request, regno):
	types=Car.objects.all()
	car=Car.objects.get(RegNo=regno)
	context={'car':car, 'types':types,}
	templatename='index/details.html'
	return render(request, templatename, context)
def validate(request):
    username = request.GET.get('username')
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)
def enter(request):
	if request.method=='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('profile')
		error="Wrong Credentials"
		types=Car.objects.all()
		templatename='index/login.html'
		context={'error':error, 'types':types,}
		return render(request, templatename, context)
	if request.user.is_authenticated:
		return redirect('profile')
	types=Car.objects.all()
	templatename='index/login.html'
	context={'types':types}
	return render(request, templatename, context)
def ajaxlogin(request):
	username = request.GET.get('username')
	password = request.GET.get('password')
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		data={'loggedin':True,}
	else:
		data={'loggedin':False,}
	return JsonResponse(data)
def ajaxregister(request):
	firstname=request.GET.get('firstname')
	secondname=request.GET.get('secondname')
	username=request.GET.get('username')
	idno=request.GET.get('idno')
	email=request.GET.get('email')
	contact=request.GET.get('contact')
	password=request.GET.get('pass1')
	client=Client()
	client.Firstname=firstname
	client.Secondname=secondname
	client.Username=username
	client.Idno=idno
	client.Contact=contact
	client.Email=email
	client.save()
	user = User.objects.create_user(username, email, password)
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request, user)
		data={'loggedin':True,}
	else:
		data={'loggedin':False,}
	return JsonResponse(data)

def register(request):
	if request.method=='POST':
		firstname=request.POST.get('firstname')
		secondname=request.POST.get('secondname')
		username=request.POST.get('username')
		idno=request.POST.get('idno')
		email=request.POST.get('email')
		contact=request.POST.get('contact')
		password=request.POST.get('pass1')
		category=request.POST.get('category')
		if Client.objects.filter(Username=username).exists() or Owner.objects.filter(Username=username).exists():
			error="Error username already taken!"
			types=Car.objects.all()
			templatename='index/register.html'
			context={'error':error, 'types':types,}
		if Client.objects.filter(Idno=idno).exists() or Owner.objects.filter(Idno=idno).exists():
			error="Error Identity No account exists!"
			types=Car.objects.all()
			templatename='index/register.html'
			context={'error':error, 'types':types,}
		if Client.objects.filter(Contact=contact).exists() or Owner.objects.filter(Contact=contact).exists():
			error="Contact account exists!"
			types=Car.objects.all()
			templatename='index/register.html'
			context={'error':error, 'types':types,}
		user = User.objects.create_user(username, email, password)
		user = authenticate(request, username=username, password=password)
		login(request, user)
		if category=="Owner":
			owner=Owner()
			owner.Firstname=firstname
			owner.Secondname=secondname
			owner.Username=username
			owner.Idno=idno
			owner.Contact=contact
			owner.Email=email
			owner.save()
			return redirect('profile')
		client=Client()
		client.Firstname=firstname
		client.Secondname=secondname
		client.Username=username
		client.Idno=idno
		client.Contact=contact
		client.Email=email
		client.save()
		return redirect('profile')
	if request.user.is_authenticated:
		return redirect('profile')
	types=Car.objects.all()
	templatename='index/register.html'
	context={'types':types}
	return render(request, templatename, context)

def search(request):
	brand=request.POST.get('brand')
	pickup=request.POST.get('pickup')
	location=PickLoc.objects.get(id=pickup)
	cars_list=Car.objects.filter(Available=True, Type=brand).filter(Location=location)
	types=Car.objects.all()
	templatename='index/search.html'
	context={'cars_list':cars_list, 'types':types, 'search':search,}
	return render(request,templatename, context)
def verify(request):
	if request.method=="POST":
		contact=request.POST.get('contact')
		if Client.objects.filter(Contact=contact).exists() or Owner.objects.filter(Contact=contact).exists():
			message=str(random.randint(1000, 9999))
			url ="https://my.jisort.com/messenger/send_message/?username=isaacmasinde2019@gmail.com&password=14414@starehe&recipients=%s&message="%contact +message
			payload = {}
			headers = {}
			response = requests.request("GET", url, headers=headers, data = payload)
			code=Code()
			code.Contact=contact
			code.Pin=str(message)
			code.save()
			types=Car.objects.all()
			context={'types':types,'contact':contact,}
			templatename='user/confirm.html'
			return render(request, templatename, context)
		else:
			types=Car.objects.all()
			error="No account with the contact exists"
			context={'types':types, 'error':error,}
			templatename='user/verify.html'
			return render(request, templatename, context)
	types=Car.objects.all()
	context={'types':types,}
	templatename='user/verify.html'
	return render(request, templatename, context)
def confirm(request):
	otp=request.POST.get('otp')
	contact=request.POST.get('contact')
	password=request.POST.get('password')
	code=Code.objects.filter(Contact=contact).last()
	pin=code.Pin
	if pin==otp:
		if Client.objects.filter(Contact=contact).exists():
			username=Client.objects.get(Contact=contact).Username
		else:
			username=Owner.objects.get(Contact=contact)
		userobj=User.objects.get(username=username)
		userobj.set_password(password)
		userobj.save()
		user=authenticate(request, username=username, password=password)
		login(request, user)
		return redirect('profile')
	templatename='user/confirm.html'
	error="Wrong One Time Pin"
	types=Car.objects.all()
	context={'types':types, 'contact':contact, 'error':error,}
	return render(request, templatename, context)

# Create your views here.