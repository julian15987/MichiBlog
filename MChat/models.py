from django.db import models
from MBlog.models import MichiProfile

# Create your models here.


class MichiRoofs(models.Model):
    roof_id = models.IntegerField(primary_key=True, blank=False, null=False)
    roof_name = models.CharField(max_length=50, blank=False, null=False)
    michi_owner = models.ForeignKey(MichiProfile, on_delete=models.CASCADE, related_name='michi_owner')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.roof_id} roof'


class MichiRoofUsers(models.Model):
    roof_id = models.ForeignKey(MichiRoofs, on_delete=models.CASCADE, blank=False, null=False)
    user_id = models.ForeignKey(MichiProfile, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_id} in roof {self.roof_id}'


class MichiRoofChats(models.Model):
    roof_id = models.ForeignKey(MichiRoofs, on_delete=models.CASCADE, blank=False, null=False)
    michi_author = models.ForeignKey(MichiProfile, on_delete=models.CASCADE, blank=True, null=True)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} - {self.message} - {self.michi_author.nickname}'
