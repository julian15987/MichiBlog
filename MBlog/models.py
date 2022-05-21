from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now
# Create your models here.


class MichiProfile(models.Model):
    """ Model class for MichiProfile, which is a user profile. """
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    hair_color = models.CharField(max_length=50)
    eye_color = models.CharField(max_length=50)
    birthday = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    erased = models.BooleanField(default=False)

    def __str__(self):
        return self.nickname


class MichiPost(models.Model):
    """ Model class for MichiPost, which is a post. """
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    michi_author = models.ForeignKey(MichiProfile, on_delete=models.CASCADE, blank=False, null=False)
    header_image = models.ImageField(upload_to='post_pictures', blank=True, null=True)
    content_image = models.ImageField(upload_to='post_pictures', blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    erased = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class MichiComments(models.Model):
    """ Model class for MichiComments, which is a comment. """
    michi_post = models.ForeignKey(MichiPost, on_delete=models.CASCADE, blank=False, null=False)
    michi_author = models.ForeignKey(MichiProfile, on_delete=models.CASCADE, blank=False, null=False)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    erased = models.BooleanField(default=False)

    def __str__(self):
        return self.content
