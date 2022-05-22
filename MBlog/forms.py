from django import forms
from .models import MichiPost


class MichiPostForm(forms.ModelForm):
    class Meta:
        model = MichiPost
        fields = ('title', 'subtitle', 'content', 'header_image', 'content_image', 'category')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titulo del post'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subtitulo del post'})
        }
