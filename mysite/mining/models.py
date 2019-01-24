from django.db import models

# Create your models here.


class Person(models.Model):
	name = models.CharField(max_length=50)
	faceimage = models.ImageField(upload_to='face')
	lasttime = models.DateField()
	def __str__(self):
		return self.name


class Log(models.Model):
	time = models.DateTimeField(auto_now_add=True, editable=False)
	address = models.CharField(max_length=512, editable=False)
	image = models.ImageField(upload_to='image_cache')
	video = models.FilePathField(max_length=512)
	message = models.CharField(maxn_length=1024)


