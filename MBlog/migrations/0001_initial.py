# Generated by Django 4.0.4 on 2022-05-21 13:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MichiProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('nickname', models.CharField(max_length=50)),
                ('hair_color', models.CharField(max_length=50)),
                ('eye_color', models.CharField(max_length=50)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pictures')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('erased', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MichiPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.CharField(max_length=255)),
                ('header_image', models.ImageField(blank=True, null=True, upload_to='post_pictures')),
                ('content_image', models.ImageField(blank=True, null=True, upload_to='post_pictures')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('erased', models.BooleanField(default=False)),
                ('michi_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MBlog.michiprofile')),
            ],
        ),
        migrations.CreateModel(
            name='MichiComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('erased', models.BooleanField(default=False)),
                ('michi_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MBlog.michiprofile')),
                ('michi_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MBlog.michipost')),
                ('parent_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MBlog.michicomments')),
            ],
        ),
    ]
