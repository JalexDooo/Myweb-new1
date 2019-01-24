from django.urls import path
from . import views

app_name = 'mining'

urlpatterns = [
	path('', views.index, name='index'),
	path('login', views.login, name='person_information_login'),
	path('register', views.register, name='person_information_register'),
	path('logout', views.logout, name='person_information_logout'),
	path('face', views.face, name="facerecognition"),
	path('addface', views.addface, name="addfaceimage"),
	path('deleteface', views.deleteface, name="deletefaceimage"),
]