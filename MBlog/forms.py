from django import forms
from .models import MichiPost, MichiProfile, PostCategories


class MichiPostForm(forms.ModelForm):
    class Meta:
        model = MichiPost
        fields = ('title', 'subtitle', 'content', 'header_image', 'content_image', 'category')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titulo del post'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subtitulo del post'})
        }


class MichiProfileForm(forms.ModelForm):
    class Meta:
        model = MichiProfile
        fields = ('nickname', 'hair_color', 'eye_color', 'birthday', 'profile_picture', 'erased')
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nickname'}),
            'hair_color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color de pelo'}),
            'eye_color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color de ojos'})
        }


class PostCategoriesForm(forms.ModelForm):
    class Meta:
        model = PostCategories
        fields = '__all__'
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoria'})
        }
