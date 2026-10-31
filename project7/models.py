from django.db import models
from django.contrib.auth.models import User

class RoomType(models.Model):
  name = models.CharField(max_length=50,verbose_name="Тип кімнати")

class Room(models.Model):
  title = models.CharField(max_length=25)
  description = models.TextField()
  room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True, verbose_name="Тип")
  price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0, verbose_name="Ціна")
  capacity = models.PositiveIntegerField(default=1, verbose_name="Вмістимість")


class Booking(models.Model):
  STATUS_CHOICES = (
    ('pending', 'Очікує підтвердження'),
    ('confirmed', 'Пітвердженно'),
    ('cancelled', 'Скасовано'),
  )
  room = models.ForeignKey(Room, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()
  status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    
  

  

# Create your models here.
