from django.db import models

class Skill(models.Model):
	'''model for skill'''
	name = models.TextField()

class User(models.Model):
	'''model for user'''
	access_level = models.IntegerField(
		default=0, choices=(0, 1, 2, 3), verbose_name='Уровень доступа')
	birthday = models.DateField(auto_now=True)

	name = models.CharField(max_length=100)
	surname = models.CharField(max_length=100)
	github = models.CharField(max_length=100, verbose_name='GITHUB')
	facebook = models.CharField(max_length=100, verbose_name='FACEBOOK')
	vk = models.CharField(max_length=100, verbose_name='VK')
	skills = models.ManyToManyField(Skill)

class Hackathon(models.Model):
	'''model for hackathon'''
	name = models.CharField(max_length=300)
	date = models.DateField()
	duration = models.DateTimeField()

class News (models.Model):
	'''class for announcement'''
	text = models.TextField()

class Invintation(models.Model):
	'''class for invitation to the hackthone'''
	from_user = models.OneToOneField(User, on_delete=models.SET_NULL)
	to_user = models.OneToOneField(User, on_delete=models.SET_NULL)
	hackathon = models.OneToOneField(Hackathon, on_delete=models.SET_NULL)

