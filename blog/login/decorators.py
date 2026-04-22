from django.shortcuts import redirect, render
from .models import User


def login_required (func):
    """
    Проверка вошел ли пользователь в систему Если нет -> на страницу логин
    """
    def wrapper (request, *args, **kwargs):
        if not request.session.get ('user_id') :
            return redirect ('/login')
        return func (request, *args, **kwargs)
    return wrapper



def is_user(func):
    @login_required
    def wrapper  (request, *args, **kwargs):
        u = None
        if request.session.get('user_id'):
            u_id = request.session.get('user_id')
            u = User.objects.get(id = u_id)
            users = User.objects.all()
            return render (request, 'users.html', {'users': users, 'user': u})
        else :
            return redirect ('/login/')
    return wrapper
        

        
def is_director(func):
    @login_required
    def wrapper (request, *args, **kwargs):
        id_user = request.session.get ('user_id')
        user = User.objects.get (id=id_user)
        if user :
            if user.role.id == 2:
                return func(request, *args, **kwargs)
            else: 
                message = 'Пользователь должен быть Директором'
        else :
             message = 'Пользователь не найден в базе'
        return render (request, 'error.html', {'message': message})
    return wrapper


def is_manage(func):
    @login_required
    def wrapper (request, *args, **kwargs):
        id_user = request.session.get ('user_id')
        user = User.objects.get (id=id_user)
        if user :
            if user.role.id == 1:
                return func(request, *args, **kwargs)
            else: 
                message = 'Пользователь должен быть Менеджером'
        else :
             message = 'Пользователь не найден в базе'
        return render (request, 'error.html', {'message': message})
    return wrapper