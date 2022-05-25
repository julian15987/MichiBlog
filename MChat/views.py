from django.shortcuts import render


# Create your views here.

# Roofs
def create_roof(request):
    return render(request, 'create_roof.html')

