# To create the captcha
from captcha.image import ImageCaptcha
# To generate a random string
from string import ascii_uppercase, ascii_lowercase, digits
from random import sample, shuffle, randint


def new_captcha():
	image = ImageCaptcha(width=250, height=130, fonts=['./Jost/static/Jost-Medium.ttf'])

	initial_password = sample(digits, randint(3, 5))
	shuffle(initial_password)
	final_password = "".join(initial_password)

	data = image.generate(final_password)

	image.write(final_password, 'output.png')
	return final_password
