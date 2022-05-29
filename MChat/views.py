from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from MChat.models import MichiRoofs
from django.template.defaulttags import register
# Create your views here.


@register.filter
def message_in_roofs(michi_roof_chats, michi_author):
    return michi_roof_chats.filter(michi_author=michi_author)


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

    open_roofs = MichiRoofs.objects.all()

    return render(request, 'chat/create_roof.html', {'options': options, 'roofs': open_roofs})


@login_required(login_url='/login')
def roof(request, roof_id):

    try:
        roof_obj = MichiRoofs.objects.get(roof_id=roof_id)
        messages = roof_obj.michiroofchats_set.all()

    except MichiRoofs.DoesNotExist:
        roof_obj = None
        messages = None

    return render(request, 'chat/roof.html', {
        'roof_name': roof_id,
        'roof': roof_obj,
        'old_messages': messages
    })


@login_required(login_url='/login')
def set_roof_name(request, roof_id):
    roof_name = request.POST.get('roof_name')
    MichiRoofs.objects.filter(roof_id=roof_id).update(roof_name=roof_name)
    return redirect(f'/chat/{roof_id}')
