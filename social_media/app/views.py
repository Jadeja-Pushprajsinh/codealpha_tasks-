from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver

def register(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('login')

    else:

        form = UserCreationForm()

    return render(
        request,
        'register.html',
        {
            'form': form
        }
    )

@login_required
def home(request):

    posts = Post.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'home.html',
        {
            'posts': posts
        }
    )

@receiver(post_save, sender=User)

def create_profile(sender,
                   instance,
                   created,
                   **kwargs):

    if created:

        Profile .objects.create(
            user=instance
        )

@login_required
def create_post(request):

    if request.method == 'POST':

        content = request.POST.get('content')

        image = request.POST.get('image')

        Post.objects.create(

            user=request.user,

            content=content,

            image=image
        )

        return redirect('home')

    return redirect('home')

@login_required
def like_post(request, post_id):

    post = Post.objects.get(id=post_id)

    liked = Like.objects.filter(

        user=request.user,

        post=post

    ).first()

    # UNLIKE

    if liked:

        liked.delete()

    # LIKE

    else:

        Like.objects.create(

            user=request.user,

            post=post
        )

    return redirect('home')

@login_required
def add_comment(request, post_id):

    if request.method == 'POST':

        post = Post.objects.get(id=post_id)

        text = request.POST.get('text')

        Comment.objects.create(

            user=request.user,

            post=post,

            text=text
        )

    return redirect('home')

@login_required
def profile(request, username):

    user_profile = User.objects.get(
        username=username
    )

    profile = Profile.objects.get(
        user=user_profile
    )

    posts = Post.objects.filter(
        user=user_profile
    ).order_by('-created_at')

    return render(

        request,

        'app/profile.html',

        {

            'profile': profile,

            'posts': posts
        }
    )
