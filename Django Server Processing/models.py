from django.db import models

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Image(BaseModel):
    name = models.CharField(max_length=500)
    imagefile = models.ImageField(upload_to='images/')
    processingf = models.ImageField(null=True, upload_to='images/processed')
    area = models.CharField(null=True, max_length=500)
    depth = models.CharField(null=True, max_length=500)
    no_of_pothole = models.CharField(null=True, max_length=500)
    lat = models.CharField(null=True, max_length=500)
    long = models.CharField(null=True, max_length=500)
