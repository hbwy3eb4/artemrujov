from django.db import models

from django.contrib.auth.models import AbstractUser

from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.username


User = get_user_model()

class Family(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class FamilyMember(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='members')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    birth_place_lat = models.FloatField(null=True, blank=True)
    birth_place_lon = models.FloatField(null=True, blank=True)
    burial_place_lat = models.FloatField(null=True, blank=True)
    burial_place_lon = models.FloatField(null=True, blank=True)
    bio = models.TextField(blank=True)
    
    # Связи
    parents = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='children')
    spouse = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='spouses')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Comment(models.Model):
    member = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.author} on {self.member}"
    

    