from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator


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
