from django.shortcuts import render


# Create your views here.

# Roofs
def create_roof(request):
    return render(request, 'chat/create_roof.html')


def roof(request, roof_name):
    return render(request, 'chat/roof.html', {
        'roof_name': roof_name
    })
