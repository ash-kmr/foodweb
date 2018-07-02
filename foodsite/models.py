from django.db import models
from django.conf import settings
import datetime
 
class UploadFile(models.Model):
    file = models.FileField(upload_to='files/')

class Apimodel(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	apikey = models.CharField(max_length=25, default=None, unique=True)
	status = models.BooleanField(default=False)
	usage = models.IntegerField(default=0)
	limit = models.IntegerField(default=500)
	resettime = models.TimeField(default=None)