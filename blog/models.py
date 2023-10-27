from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
from ckeditor.fields import RichTextField

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone_no = models.IntegerField(blank=True, null=True)
    facebook = models.CharField(max_length=300, blank=True, null=True)
    instagram = models.CharField(max_length=300, blank=True, null=True)
    linkedin = models.CharField(max_length=300, blank=True, null=True)
    
    def __str__(self):
        return str(self.user)

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug=models.CharField(max_length=130)
    # content = RichTextField(blank=True, null=True)
    content = models.TextField(default=None)
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    category = models.CharField(max_length=100, default='categorised')
    

    def __str__(self):
        return(self.title)
    
    def get_absolute_url(self):
        return reverse('home')
    
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return(self.name)
    
    def get_absolute_url(self):
        return reverse('home')
    
class About(models.Model):
    content = models.TextField()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,)
    content = models.TextField()
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')   
    created_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.user.username +  " Comment: " + self.content
    


