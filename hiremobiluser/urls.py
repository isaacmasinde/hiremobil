from django.urls import path
from .views import *

urlpatterns=[
	path('profile/', profile, name='profile'),
	path('logout/', out, name='logout'),
	path('reset/', reset, name='reset'),
	path('messages/', message, name='messages'),
	path('bookings/', bookings, name='bookings'),
	path('cars/', cars, name='cars'),
	path('add/', add, name='add'),
	path('config/',stripe_config, name='config'),
	path('create-checkout-session/', create_checkout_session),
	path('success/', success, name='success')
]