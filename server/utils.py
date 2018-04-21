from .models import UserRating


# users rating
def rating(rate):
	user_hack_rating = float(rate.android) + float(rate.ar) + float(rate.backend) + float(rate.blockchain) \
		+ float(rate.d2) + float(rate.d3) + float(rate.design) + float(rate.frontend) + float(rate.ios) \
		+ float(rate.management) + float(rate.ml)
	return user_hack_rating


def get_user_rating(user):
	try:
		return rating(UserRating.objects.get(user_id=user.id))
	except:
		return -1000