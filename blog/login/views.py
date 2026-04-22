from django.shortcuts import render, redirect
from .forms import UserForm, RoleForm
from .models import User
from .decorators import login_required, is_director, is_manage, is_user


def index (request):
    if request.session.get('user_id'):
        u_id = request.session.get('user_id')
        u = User.objects.get(id = u_id)
        return render (request, 'index.html', {'user': u})
    else :
        return redirect ('/login/')
    
@is_manage
def for_manage (request):
    return render (request, 'page_for_manage.html')

    
@is_director
def for_director (request):
    id_user = request.session.get ('user_id')
    user = User.objects.get (id=id_user)
    return render (request, 'page_for_director.html', {'user': user})


@login_required
def for_auth (request):
    return render (request, 'page_for_auth.html')

def logout_view (request):
    request.session.flush()
    return redirect ('/login')


def login (request) :
    if request.method == "GET":
        return render (request, 'login.html')
    else:
        login = request.POST.get('login')
        password = request.POST.get('pas')

        try:
            user = User.objects.get(login=login)
        except User.DoesNotExist:
            return redirect ('/login')
        
    if password != user.password:
        return redirect ('/login')
    

    request.session['user_id'] = user.id
    request.session['login'] = user.login
    return redirect ('/')

def add_role (request):
    if request.method == "POST":
        role = RoleForm(request.POST)
        if role.is_valid():
            role.save()
        return redirect('/users/')
    else :
        form =RoleForm()
        return render (request, "add_user.html", {'form': form})
    

@login_required
def users (request):
    users = User.objects.all()
    return render (request, 'users.html', {'users': users})



def add_user(request):
    if request.method == "POST":
        user = UserForm(request.POST)
        if user.is_valid():
            user.save()
        return redirect('/users/')
    else :
        form =UserForm()
        return render (request, "add_user.html", {'form': form})


