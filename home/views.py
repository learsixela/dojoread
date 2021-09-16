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

def cambiar_pass(request):
    reg_user = User.objects.filter(id=request.session['user_id'])
    context = {
        "active_user": reg_user,
    }

    if len(request.POST['pass_actual']) == 0:
        messages.error(request, "Debes ingresar tu contraseña actual")
        return render(request, 'recuperar.html',context)

    errores = User.objects.validar_login(request.POST['pass_actual'], reg_user)



    if len(errores) > 0:
        for key, msg in errores.items():
            messages.error(request, msg)
        return render(request, 'recuperar.html',context)
    
    if len(request.POST['pass_nueva']) == 0 or len(request.POST['pass_confirmacion']) == 0:
        messages.error(request, "Debes ingresar tu nueva contraseña")
        return render(request, 'recuperar.html',context)
    elif request.POST['pass_nueva'] != request.POST['pass_confirmacion']:
        messages.error(request, "Las contraseñas no coinciden")
        return render(request, 'recuperar.html', context)
    else:
        reg_user[0].password = User.objects.encriptar(request.POST['pass_nueva']).decode('utf-8')
        reg_user[0].save()
        request.session.flush()
        return redirect('/')
    #validar el password actual


    return render(request, 'recuperar.html', context)