from django.contrib import admin
from .models import MichiComments, MichiPost, MichiProfile

# Register your models here.

admin.site.register(MichiComments)
admin.site.register(MichiPost)
admin.site.register(MichiProfile)
