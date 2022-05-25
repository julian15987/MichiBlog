from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.

# Roofs
@login_required(login_url='/login')
def create_roof(request):
    return render(request, 'chat/create_roof.html')


@login_required(login_url='/login')
def roof(request, roof_name):
    return render(request, 'chat/roof.html', {
        'roof_name': roof_name
    })
