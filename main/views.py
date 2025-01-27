from django.shortcuts import render, redirect

from main.forms import RegistrationForm, PostForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from . models import Post
from django.contrib.auth.models import User, Group
# Create your views here.

@login_required(login_url='/login')
def home(request):
    post = Post.objects.all()
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        user_id = request.POST.get('user_id')
        if post_id:
            delPost = Post.objects.filter(id=post_id).first()
            if delPost and delPost.author == request.user or request.user.has_perm('main.delete_post'):
                delPost.delete()
        elif user_id:
            user = User.objects.filter(id=user_id).first()
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name='default')
                    group.user_set.remove(user)
                except:
                    pass
                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except:
                    pass


    return render(request, 'main/home.html', {'post': post}) 




@login_required(login_url='/login')
@permission_required('main.add_post', login_url='/login', raise_exception=True)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/home')
    else:
        form = PostForm()
    
    return render(request, 'main/create_post.html', {'form': form})




def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegistrationForm()

    return render(request, 'registration/sign_up.html', {'form': form})


