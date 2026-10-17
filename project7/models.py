from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
  title = models.CharField(max_length=25)
  description = models.TextField()


class Booking(models.Model):
  room = models.ForeignKey(Room, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()
    
  

  

# Create your models here.
