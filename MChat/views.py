from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.

# Roofs
@login_required(login_url='/login')
def create_roof(request):

    options = {
        'pescado': 'ion:fish-sharp',
        'garrita': 'icons8:cat-footprint',
        'github': 'akar-icons:octocat-fill',
        'tom': 'simple-icons:apachetomcat',
        'raton': 'emojione-monotone:mouse-face',
        'pelota': 'ph:soccer-ball-bold'
    }
    return render(request, 'chat/create_roof.html', {'options': options})


@login_required(login_url='/login')
def roof(request, roof_name):
    return render(request, 'chat/roof.html', {
        'roof_name': roof_name
    })
