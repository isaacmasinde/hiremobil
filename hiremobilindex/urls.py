from django.urls import path
from .views import *
from hiremobiluser.views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
	path('', index, name='index'),
	path('detail/<str:regno>/', detail, name='detail'),
	path('validate/', validate, name='validate'),
	path('ajaxlogin/', ajaxlogin, name='ajaxlogin'),
	path('ajaxregister/', ajaxregister, name='ajaxregister'),
	path('search/', search, name='search'),
	path('enter/', enter, name='enter'),
	path('register/', register, name='register'),
	path('verify/', verify, name='verify'),
	path('confirm/', confirm, name='confirm'),
	path('remove/<str:car>/', remove, name='remove'),
	path('book/', book, name='book')
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)