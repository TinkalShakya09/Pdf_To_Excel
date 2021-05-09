from django.db import models

# Create your models here.
class f3App(models.Model):
    file = models.FileField(upload_to='documents/')