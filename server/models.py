from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Skill(models.Model):
	'''model for skill'''
	name = models.CharField(max_length=500)

class Profile(models.Model):
	'''model for Profile'''
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	access_level = models.IntegerField(
		default=0, verbose_name='Уровень доступа')
	birthday = models.DateField(auto_now=True)

	name = models.CharField(max_length=100)
	surname = models.CharField(max_length=100)
	github = models.CharField(max_length=100, verbose_name='GITHUB')
	facebook = models.CharField(max_length=100, verbose_name='FACEBOOK')
	vk = models.CharField(max_length=100, verbose_name='VK')
	skills = models.ManyToManyField(Skill)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Hackathon(models.Model):
	'''model for hackathon'''
	name = models.CharField(max_length=300)
	description = models.CharField(max_length=5000)
	date = models.DateField()
	duration = models.DateTimeField()

class News (models.Model):
	'''class for announcement'''
text = models.CharField(max_length=2000)

class Invintation(models.Model):
	'''class for invitation to the hackthone'''
	from_Profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='from_Profile')
	to_Profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='to_Profile')
	hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='hackathon')
	date = models.DateField(auto_now=True)

