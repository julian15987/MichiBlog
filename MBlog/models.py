from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class MichiProfile(models.Model):
    """ Model class for MichiProfile, which is a user profile. """
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)
    nickname = models.CharField(max_length=50)
    hair_color = models.CharField(max_length=50)
    eye_color = models.CharField(max_length=50)
    birthday = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    erased = models.BooleanField(default=False)

    def __str__(self):
        return f'Profile of {self.user.username}'


class MichiPost(models.Model):
    """ Model class for MichiPost, which is a post. """
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    michi_author = models.ForeignKey(MichiProfile, on_delete=models.CASCADE, blank=False, null=False)
    header_image = models.ImageField(upload_to='post_pictures', blank=True, null=True)
    content_image = models.ImageField(upload_to='post_pictures', blank=True, null=True)
    content = models.TextField()
    category = models.ForeignKey('PostCategories', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    erased = models.BooleanField(default=False)

    def __str__(self):
        return f'Post {self.id} by {self.michi_author.nickname}'


class MichiStars(models.Model):
    """ Model class for MichiStars, which is a star rating for a post by a Michi. """
    michi_post = models.ForeignKey(MichiPost, on_delete=models.CASCADE, blank=False, null=False)
    michi_author = models.ForeignKey(MichiProfile, on_delete=models.CASCADE, blank=False, null=False)
    stars = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)], blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.stars } stars by {self.michi_author.nickname} in post {self.michi_post.id}'


class PostCategories(models.Model):
    """ Model class for PostCategories, which is a category for a post. """
    category = models.CharField(max_length=50)

    def __str__(self):
        return f'Category {self.category}'


class MichiComments(models.Model):
    """ Model class for MichiComments, which is a comment. """
    michi_post = models.ForeignKey(MichiPost, on_delete=models.CASCADE, blank=False, null=False)
    michi_author = models.ForeignKey(MichiProfile, on_delete=models.CASCADE, blank=False, null=False)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    erased = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment by {self.michi_author.nickname} on {self.michi_post.title}'
