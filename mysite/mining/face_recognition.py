import os
import face_recognition as fr
import cv2
import time
import itertools
from PIL import Image, ImageDraw, ImageFont
import multiprocessing
import numpy as np

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
			for name in sub_folders:
				temp.append(os.path.join(root, name))
		i = 0
		for one_folder in temp:
			label = one_folder.split('/')[-1]
			labels = np.append(labels, label)
			i += 1
		temp = np.array([images, labels])
		image_list = list(temp[0])
		label_list = list(temp[1])

		return image_list, label_list

#########################################################################

def thread(id, label_list, known_faces):
	# for id in index_th:
	video_catch = cv2.VideoCapture(id)
	# video_catch.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280);
	# video_catch.set(cv2.CAP_PROP_FRAME_WIDTH, 960);
	# video_catch.set(cv2.CAP_PROP_FPS, 30.0);


	face_locations = []
	face_encodings = []
	face_names = []
	frame_number = 0
	print('%d isOpened!'%id, video_catch.isOpened())
	if not video_catch.isOpened():
		return
	while True:
		ret, frame = video_catch.read()
		# print('%s' % id, ret)

		frame_number += 1
		if not ret:
			break
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

		for (top, right, bottom, left), name in zip(face_locations, face_names):
			if not name:
				continue
			top *= 4
			right *= 4
			bottom *= 4
			left *= 4

			pil_im = Image.fromarray(frame)
			draw = ImageDraw.Draw(pil_im)
			font = ImageFont.truetype('/home/jonty/Documents/sources/STHeiti Medium.ttc', 24,
									  encoding='utf-8')
			draw.text((left + 6, bottom - 25), name, (0, 0, 255), font=font)

			frame = np.array(pil_im)
			cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
		cv2.imshow('Video_%s' % id, frame)

		c = cv2.waitKey(1)
		if c & 0xFF == ord("q"):
			break

	video_catch.release()
	cv2.destroyWindow('Video_%s' % id)


class multiprocessing_face_recognition(object):
	"""docstring for multiprocessing_face_recognition"""
	def __init__(self, number_of_cpu, num_cam_list, label_list, known_faces):
		super(multiprocessing_face_recognition, self).__init__()
		self.number_of_cpu = number_of_cpu
		self.label_list = label_list
		self.known_faces = known_faces
		self.num_cam_list = num_cam_list

		self.process_images_in_process_pool(self.num_cam_list, self.number_of_cpu, self.label_list, self.known_faces)

	def process_images_in_process_pool(self, index_th, number_of_cpus, label_list, known_faces):
		if number_of_cpus == -1:
			processes = None
		else:
			processes = number_of_cpus

		# macOS will crash due to a bug in libdispatch if you don't use 'forkserver'
		context = multiprocessing
		if "forkserver" in multiprocessing.get_all_start_methods():
			context = multiprocessing.get_context("forkserver")

		pool = context.Pool(processes=processes)

		function_parameters = zip(
			index_th,
			itertools.repeat(label_list),
			itertools.repeat(known_faces),
		)

		pool.starmap(thread, function_parameters)
		





#########################################################################

def face_recognition(number_of_cpu):
	path = '/home/jonty/Documents/Project_2018/database/face_recognition_database'
	face_database = get_file(path)
	image_list, label_list = face_database.func()

	known_faces = []
	for i in range(len(image_list)):
		tmp = fr.load_image_file(image_list[i])
		known_faces.append(list(fr.face_encodings(tmp)[0]))

	num_camera = 2 #######################
	num_cam_list = []
	for i in range(num_camera):
		num_cam_list.append(i)

	print(num_cam_list)
	main_face = multiprocessing_face_recognition(number_of_cpu, num_cam_list, label_list, known_faces)



if __name__ == '__main__':
	face_recognition = face_recognition(-1)