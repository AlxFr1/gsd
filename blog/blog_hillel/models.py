from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1000, help_text='Blogger biography', blank=True)
    profile_picture = models.ImageField(null=True, blank=True, default='unknown_user.jpg')

    class Meta:
        verbose_name_plural = 'User'

    def __str__(self):
        return f'{self.user.username}'

    def get_absolute_url(self):
        return reverse('profile-detail', args=[str(self.id)])


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    descript = models.TextField(max_length=3000)
    image = models.ImageField(null=True, blank=True)
    pub_date = models.DateTimeField(auto_now=True)
    is_posted = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def get_date(self):
        return f'{self.pub_date.strftime("%b")} {self.pub_date.day}, {self.pub_date.year}'

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    user_name = models.CharField(max_length=50, default='Anonymous')
    text = models.TextField()

    def __str__(self):
        return f'{self.user_name}'
