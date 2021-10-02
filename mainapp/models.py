from django.db import models

# Create your models here.


class HomeLocation(models.Model):
	name = models.CharField(max_length=255)
	image = models.ImageField(upload_to='home_locations/')

	def __str__(self):
		return self.name

	def get_name(self):
		return self.name.replace('-', ' ')

class HomeBackground(models.Model):
	image = models.ImageField(upload_to='home_background/')

	def __str__(self):
		return self.image.name