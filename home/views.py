from django.shortcuts import render, redirect
from django.contrib import messages
from login.models import User, Autor, Libro


# Create your views here.
def home(request):
    reg_user = User.objects.get(id=request.session['user_id'])

    context = {
        "active_user": reg_user,
    }

    return render(request, 'home.html', context)

def agregar(request):
    return render(request, 'agregar.html')

def insertar(request):
    errores = {}

    if int(request.post['sautor'])!=0:
        autor = Autor.objects.get(id=request.post['sautor'])
    elif len(request.post['autor'])!=0:
        autor = Autor.objects.create(nombre=request.post['autor'])
    else:
        errores['autor'] = "Selecciona o crea un autor"
    
    if len(request.post['titulo']) == 0:
        errores['titulo'] = "debes agregar un titulo"
    
    if len(request.post['review']) == 0:
        errores['review'] = "debes agregar un review"

    if int(request.post['rating']) == 0:
        errores['rating'] = "debes seleccionar un rating"

    if len(errores) > 0:
        for key, msg in errores.items():
            messages.error(request, msg)
        return render(request, 'agregar.html')
    else:
        libro = Libro.objects.create(titulo=request.post['titulo'], autor=autor)
        return redirect('/home')

    return render(request, 'agregar.html')

def recuperar(request):
    reg_user = User.objects.get(id=request.session['user_id'])

    context = {
        "active_user": reg_user,
    }
    return render(request, 'recuperar.html', context)