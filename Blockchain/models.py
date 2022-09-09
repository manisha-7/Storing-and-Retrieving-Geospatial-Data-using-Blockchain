from django.db import models
import datetime
from mongoengine import Document, fields
# Create your models here.
class file_upload(models.Model):
    TYPE =(
        ('Image','Image'),
        ('Audio','Audio'),
        ('Video','Video')
    )
    ids = models.AutoField(primary_key=True)
    Coordinate = models.CharField(max_length=255)
    date = models.DateField()
    Location = models.CharField(max_length=255,default= 'hubli')
    Satellite = models.CharField(max_length=255, default='1')
    type_of_data=models.CharField(max_length=100,null =True,choices=TYPE, default='Any')
    my_file = models.FileField(upload_to='')
    
    def __str__(self):
        return self.Coordinate
    
class isro123(models.Model):
    # ids = models.AutoField(primary_key=True)
    block = models.CharField(primary_key=True, max_length=255, default='123')
    # date = models.DateField(default=datetime.date.today())
    # Location = models.CharField(max_length=255,default= 'hubli')
    # Satellite = models.CharField(max_length=255, default='1')
    # type_of_data=models.CharField(max_length=100,null =True,choices=TYPE, default='Any')
    # def __str__(self):
    #     return self.Coordinate