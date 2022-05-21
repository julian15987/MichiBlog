from django.contrib import admin
from .models import MichiComments, MichiPost, MichiProfile, PostCategories, MichiStars

# Register your models here.

admin.site.register(MichiComments)
admin.site.register(MichiPost)
admin.site.register(MichiProfile)
admin.site.register(PostCategories)
admin.site.register(MichiStars)
