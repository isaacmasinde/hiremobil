from django.shortcuts import render, redirect
from .models import *
from django.http import *
from django.conf import settings
from django.db.models import *
from django.contrib.auth.models import *
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from hiremobilindex.models import *
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import stripe

@login_required(login_url='/enter/')
def profile(request):
	if request.user.is_staff:
		return redirect('/chief/')
	if Client.objects.filter(Username=request.user.username).exists():
		client=Client.objects.get(Username=request.user.username)
		confirmed=Deal.objects.filter(Client=client, Status="Approved").count()
		pending=Deal.objects.filter(Client=client, Status="Pending").count()
		context={'client':client, 'confirmed':confirmed,'pending':pending}
		templatename='user/profile.html'
		return render(request, templatename, context)
	else:
		client=Owner.objects.get(Username=request.user.username)
		confirmed=Deal.objects.filter(Saler=client, Status="confirmed").count()
		pending=Deal.objects.filter(Saler=client, Status="pending").count()
		vehicles=Car.objects.filter(Owner=client).count()
		context={'client':client, 'confirmed':confirmed,'pending':pending, 'vehicles':vehicles}
		templatename='owner/profile.html'
		return render(request, templatename, context)


def out(request):
	logout(request)
	return redirect('index')

@login_required(login_url='/enter/')
def reset(request):
	if request.method=="POST":
		oldpass=request.POST.get('oldpass')
		newpass=request.POST.get('newpass')
		username=request.user.username
		user=authenticate(request, username=username, password=oldpass)
		if user is not None:
			login(request, user)
			userobj=User.objects.get(username=username)
			userobj.set_password(newpass)
			userobj.save()
			user=authenticate(request, username=username, password=newpass)
			login(request, user)
			types=Car.objects.all()
			context={'types':types,}
			return render(request, 'user/resetok.html', context)
		else:
			types=Car.objects.all()
			error="Your old password is wrong retry!"
			context={'types':types, 'error':error,}
			templatename='user/reset.html'
			return render(request, templatename, context)
	types=Car.objects.all()
	context={'types':types,}
	templatename='user/reset.html'
	return render(request, templatename, context)
@login_required(login_url='/enter/')
def message(request):
    username=request.user.username
    if Client.objects.filter(Username=username).exists():
    	templatename='user/messages.html'
    else:
    	templatename='owner/messages.html'
    Messages=Message.objects.all()
    context={'Messages':Messages,}
    return render(request, templatename, context)
@login_required(login_url='/enter/')
def bookings(request):
	username=request.user.username
	if Client.objects.filter(Username=username).exists():
		client=Client.objects.get(Username=username)
		context={'client':client,}
		return render(request, 'user/bookings.html', context)
	else:
		client=Owner.objects.get(Username=username)
		context={'client':client,}
		return render(request, 'owner/bookings.html', context)
@login_required(login_url='/enter/')
def cars(request):
	owner=Owner.objects.get(Username=request.user.username)
	context={'owner':owner,}
	return render(request, 'owner/vehicles.html', context)
def remove(request, car):
	vehicle=Car.objects.get(RegNo=car)
	vehicle.delete()
	return redirect('cars')
@login_required(login_url='/enter/')
def add(request):
	if request.method=='GET':
		locations=PickLoc.objects.all()
		context={'locations':locations,}
		templatename='owner/addcar.html'
		return render(request, templatename , context)
	else:
		regno=request.POST.get('regno')
		type=request.POST.get('type')
		model=request.POST.get('model')
		modelyear=request.POST.get('modelyear')
		condition=request.POST.get('condition')
		mileage=request.POST.get('mileage')
		fee=request.POST.get('fee')
		desc=request.POST.get('desc')
		location=request.POST.get('location')
		pic = request.FILES['pic']
		fs = FileSystemStorage()
		filename = fs.save(pic.name, pic)
		file_url = fs.url(filename)
		owner=Owner.objects.get(Username=request.user.username)
		lock=PickLoc.objects.get(Name=location)
		car=Car()
		car.RegNo=regno
		car.Type=type
		car.Model=model
		car.ModelYear=modelyear
		car.Condition=condition
		car.Mileage=mileage
		car.Fee=fee
		car.Description=desc
		car.Pic=filename
		car.Location=lock
		car.Owner=owner
		car.Available=False
		car.save()
		context={'car':car,}
		templatename='owner/payment.html'
		return render(request, templatename, context)
@login_required(login_url='/enter/')
def book(request):
	fro=request.POST.get('from')
	to=request.POST.get('to')
	charge=request.POST.get('fee')
	regno=request.POST.get('regno')
	car=Car.objects.get(RegNo=regno)
	deal=Deal()
	client=Client.objects.get(Username=request.user.username)
	deal.Client=client
	deal.Saler=car.Owner
	deal.Location=car.Location
	deal.Date=fro
	deal.To=to
	deal.Status="Approved"
	deal.Car=car
	deal.Charge=int(charge)
	deal.save()
	car.Available=False
	car.save()
	try:
		contact=deal.Saler.Contact
		message='Hello %s someone has requested to hire your car please check your hiremobil  account for booking details.'%deal.Saler.Username
		url ="https://my.jisort.com/messenger/send_message/?username=isaacmasinde2019@gmail.com&password=14414@starehe&recipients=%s&message="%contact +message
		payload = {}
		headers = {}
		response = requests.request("GET", url, headers=headers, data = payload)
	except:
		pass
	return redirect('bookings')

def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://127.0.0.1:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'account/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'account/profile/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'Car',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': '1000',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
def success(request):
	username=request.user.username
	owner=Owner.objects.get(Username=username)
	car=Car.objects.filter(Owner=owner, Available=False).first()
	car.Available=True
	car.save()
	return redirect('cars')




# Create your views here