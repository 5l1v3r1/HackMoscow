from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator

import matplotlib.pyplot as plt
import numpy as np
from math import pi
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
import os

class Skill(models.Model):
	'''model for skill'''
	name = models.CharField(max_length=500)


class Tag(models.Model):
	'''model for hackathon tags '''
	tagname = models.CharField(max_length=30, default="[Undefinded]")
	def __str__(self):
		return self.tagname


class Profile(models.Model):
	'''model for Profile'''
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(upload_to='uploads/', default = 'unknown_img.jpg')
	access_level = models.IntegerField(
		default=0, verbose_name='Уровень доступа')
	birthday = models.DateField(auto_now=True)
	name = models.CharField(max_length=100)
	surname = models.CharField(max_length=100)
	github = models.CharField(max_length=100)
	facebook = models.CharField(max_length=100)
	vk = models.CharField(max_length=100)
	skills = models.ManyToManyField(Skill)


class Hackathon(models.Model):
	'''model for hackathon'''
	name = models.CharField(max_length=300)
	description = models.CharField(max_length=5000, default="")
	date = models.DateField()
	users = models.ManyToManyField(User)
	duration = models.IntegerField(validators=[MinValueValidator(1), ])
	max_members = models.IntegerField(validators=[MinValueValidator(1), ])
	tags = models.ManyToManyField(Tag, related_name="tags", verbose_name='Теги')

	@property
	def hack_url(self):
		return "/hack_info/{0}".format(self.id)


class News(models.Model):
	'''class for announcement'''
	text = models.CharField(max_length=2000)


class Invintation(models.Model):
	'''class for invitation to the hackthone'''
	from_Profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='from_Profile')
	to_Profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='to_Profile')
	hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='hackathon')
	date = models.DateField(auto_now=True)


class Team(models.Model):
	'''class for team'''
	name = models.CharField(max_length=100)
	users = models.ManyToManyField(User)
	hackathones = models.ManyToManyField(Hackathon)

class UserRating(models.Model):
	frontend = models.FloatField(default=0)
	backend = models.FloatField(default=0)
	ml = models.FloatField(default=0)
	management = models.FloatField(default=0)
	design = models.FloatField(default=0)
	ar = models.FloatField(default=0)
	blockchain = models.FloatField(default=0)
	user = models.OneToOneField(Profile, on_delete=models.CASCADE)
	android = models.FloatField(default=0)
	ios = models.FloatField(default=0)
	d2 = models.FloatField(default=0)
	d3 = models.FloatField(default=0)

	@property
	def diagram(self):
		fig = plt.Figure()
		labels = ['frontend', 'backend', 'ml', 'management', 'design', 'ar', 'blockchain', 'android', 'ios']
		values = [self.user.userrating.frontend, self.user.userrating.backend, self.user.userrating.ml, self.user.userrating.management,
				  self.user.userrating.design, self.user.userrating.ar, self.user.userrating.blockchain, self.user.userrating.android, self.user.userrating.ios]
		N = len(labels)

		x_as = [n / float(N) * 2 * pi for n in range(N)]
		values += values[:1]
		x_as += x_as[:1]
		plt.rc('axes', linewidth=0.5, edgecolor="#888888")

		# Create polar plot
		ax = plt.subplot(111, polar=True)
		# Set clockwise rotation. That is:
		ax.set_theta_offset(pi / 2)
		ax.set_theta_direction(-1)

		# Set position of y-labels
		ax.set_rlabel_position(0)

		# Set color and linestyle of grid
		ax.xaxis.grid(True, color="#888888", linestyle='solid', linewidth=0.5)
		ax.yaxis.grid(True, color="#888888", linestyle='solid', linewidth=0.5)
		# Set number of radial axes and remove labels
		plt.xticks(x_as[:-1], [])

		plt.yticks([5, 10, 15, 20], ["5", "10", "15", "20"])

		# Plot data
		ax.plot(x_as, values, linewidth=0, linestyle='solid', zorder=3)

		# Fill area
		ax.fill(x_as, values, 'b', alpha=0.3)

		# Set axes limits
		plt.ylim(0, 20)

		# Draw ytick labels to make sure they fit properly
		for i in range(N):
			angle_rad = i / float(N) * 2 * pi

			if angle_rad == 0:
				ha, distance_ax = "center", 10
			elif 0 < angle_rad < pi:
				ha, distance_ax = "left", 1
			elif angle_rad == pi:
				ha, distance_ax = "center", 1
			else:
				ha, distance_ax = "right", 1

			ax.text(angle_rad, 20 + distance_ax, labels[i], size=10, horizontalalignment=ha,
					verticalalignment="center")
		url = 'media/dia'+ str(self.user.id) + '.jpg'
		plt.savefig(url)
		plt.close()

		return url


class Achievement(models.Model):
	'''class fot achievement'''
	user = models.ManyToManyField(Profile)
	image = models.ImageField()
	info = models.CharField(max_length=1000)


RATES = ((1, 'Very bad'), (2, 'Bad'), (3, 'Medium'), (4, 'Good'), (5, 'Perfect'))


class HackRateByUser(models.Model):
	'''model for rates by User'''
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	hack = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
	rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], choices=RATES)
	comment = models.CharField(max_length=1000)


