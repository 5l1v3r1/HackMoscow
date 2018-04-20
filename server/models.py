from django.db import models

class Skill(models.Model):
	'''model for skill'''
	name = models.CharField(max_length=500)

class User(models.Model):
	'''model for user'''
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
	date = models.DateField()
	duration = models.DateTimeField()

class News (models.Model):
	'''class for announcement'''
text = models.CharField(max_length=2000)

class Invintation(models.Model):
	'''class for invitation to the hackthone'''
	from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
	to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
	hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='hackathon')
	date = models.DateField(auto_now=True)

