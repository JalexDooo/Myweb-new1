from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import base64
import numpy as np
import cv2
import os
import face_recognition as fr
import cv2
import time
import itertools
from PIL import Image, ImageDraw, ImageFont
from .models import Person
###### init

class get_file(object):
	"""docstring for get_file"""
	def __init__(self, file_dir):
		super(get_file, self).__init__()
		self.file_dir = file_dir

	def func(self):
		image_rule = ['png', 'jpg', 'jpeg']
		labels = []
		images = []
		temp = []
		for root, sub_folders, files in os.walk(self.file_dir):
			for name in files:
				if name.split('.')[-1] in image_rule:
					images.append(os.path.join(root, name))
					# print(name)
					labels.append(name.split('_')[0])
		# 	for name in sub_folders:
		# 		temp.append(os.path.join(root, name))
		# i = 0
		# print(images)
		# for one_folder in temp:
		# 	label = one_folder.split('/')[-1]
		# 	labels = np.append(labels, label)
		# 	i += 1
		temp = np.array([images, labels])
		image_list = list(temp[0])
		label_list = list(temp[1])

		return image_list, label_list

path = '/home/jonty/Documents/Project_2018/database/face_recognition_database'
face_database = get_file(path)
image_list, label_list = face_database.func()
known_faces = []
for i in range(len(image_list)):
	tmp = fr.load_image_file(image_list[i])
	known_faces.append(list(fr.face_encodings(tmp)[0]))

def recognition_face(frame):
	face_locations = []
	face_encodings = []
	face_names = []
	frame_number = 0

	small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
	rgb_frame = small_frame[:, :, ::-1]

	face_locations = fr.face_locations(rgb_frame, model='cnn')  # ,model="cnn"
	face_encodings = fr.face_encodings(rgb_frame, face_locations)

	face_names = []

	for face_encoding in face_encodings:
		match = fr.compare_faces(known_faces, face_encoding, tolerance=0.425)

		name = "???"
		for i in range(len(label_list)):
			if match[i]:
				name = label_list[i]

		face_names.append(name)

	return face_names

print(label_list)





#############################################################################

# Create your views here.

def index(request):
	# user_list = superuser.objects.all()
	# context = {'user_list': user_list}
	return render(request, 'index.html')

# def login(request):
# 	return render(request, 'personcontrol/login.html')

# def loginVerify(request):
# 	if request.method = 'POST':
# 		username = request.POST['username']
# 		password = request.Post['id-password']
# 		users = superuser.objects.all()

# 		for user in users:
# 			if user.username == username and user.password == password:
# 				user_list = superuser.objects.all()
# 				context = {'user_list': user_list}
# 				return HttpResponse('1')
# 		return HttpResponse('-1')


def logout(request):
	auth.logout(request)
	return render(request, 'index.html')


@csrf_exempt
def login(request):
	errors = []
	account = None
	password = None

	if request.method == 'POST':

		if not request.POST.get('account'):
			errors.append('Username is empty!')
		else:
			account = request.POST.get('account')

		if not request.POST.get('password'):
			errors.append('Password is empty!')
		else:
			password = request.POST.get('password')

		if account is not None and password is not None:
			user = auth.authenticate(username=account, password=password)

			if user is not None:
				if user.is_active:
					auth.login(request, user)
					return render(request, 'index.html')
				else:
					errors.append('username is error!')
			else:
				errors.append('username or password is error!')

	return render(request, 'personcontrol/login.html')



@csrf_exempt
def register(request):
	errors = []
	account = None
	password = None
	password2 = None
	email = None
	CompareFlag = False


	if request.method == 'POST': # and request.name == 'login-form':
		if not request.POST.get('account'):
			errors.append('Username is empty!')
		else:
			account = request.POST.get('account')

		if not request.POST.get('password'):
			errors.append('Password is empty!')
		else:
			password = request.POST.get('password')

		if not request.POST.get('password2'):
			errors.append('Password-verified is empty!')
		else:
			password2 = request.POST.get('password2')

		if not request.POST.get('email'):
			errors.append('Email is empty!')
		else:
			email = request.POST.get('email')

		if password is not None:
			if password == password2:
				CompareFlag = True
			else:
				errors.append('password is not verified!')


		if account is not None and password is not None and password2 is not None and email is not None:
			user = User.objects.create_user(account, email, password)
			user.save()

			userlogin = auth.authenticate(username = account, password = password)
			auth.login(request, userlogin)
			return render(request, 'index.html')



	return render(request, 'personcontrol/register.html')


@csrf_exempt
def face(request):
	if request.method == 'POST':
		img_b64 = request.POST.get('facerecognition1')
		# print("hello")
		img_byt = base64.b64decode(img_b64)

		img_arr = np.fromstring(img_byt, np.uint8)
		img = cv2.imdecode(img_arr, 1)
		name_list = recognition_face(img)

		# cv2.imshow('image', img)
		print(name_list)

	return render(request, 'face/facerecognition.html')


@csrf_exempt
def addface(request):
	
	return render(request, 'face/addface.html')


@csrf_exempt
def deleteface(request):
	faceimg = Person.objects.all()
	
	return render(request, 'face/deleteface.html', {'img': faceimg})

