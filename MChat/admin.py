from django.contrib import admin
from .models import MichiRoofs, MichiRoofUsers, MichiRoofChats

# Register your models here.

admin.site.register(MichiRoofs)
admin.site.register(MichiRoofUsers)
admin.site.register(MichiRoofChats)
