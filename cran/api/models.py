# import the standard Django Model
from django.db import models


class Package(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	package_name = models.CharField(max_length=100)

	def __str__(self):
		return self.title