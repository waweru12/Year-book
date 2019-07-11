from django.db import models
from django.contrib.auth.models import User

        
class Project(models.Model):
    title = models.CharField(max_length=150)
    upload_your_images_here = models.ImageField(upload_to='landing/')
    description = models.CharField(max_length=255)
    Class_year = models.CharField(max_length=255)
    overall = models.IntegerField(blank=True,default=0)
    
    posted  = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @classmethod
    def search_project(cls, search_term):
        projects = cls.objects.filter(title__icontains=search_term)
        return projects

class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    profilepic = models.ImageField(upload_to='profiles/')
    bio = models.CharField(max_length=255)
    prefname = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)

    def __str__(self):
        return self.prefname

class Rating(models.Model):
    CHOICES = (1, 1),(2, 2),(3, 3),(4, 4),(5, 5),(6, 6),(7, 7),(8, 8),(9, 9),(10, 10)

    
    class_of_the_year = models.IntegerField(choices=CHOICES, blank=True,default=0)
    overall_score = models.IntegerField(blank=True,default=0)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE) 