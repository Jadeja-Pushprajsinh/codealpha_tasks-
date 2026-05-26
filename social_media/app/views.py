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


    if liked:

        liked.delete()

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

    profile, created = Profile.objects.get_or_create(
        user=user_profile
    )
    
    posts = Post.objects.filter(
        user=user_profile
    ).order_by('-created_at')

    is_following = Follow.objects.filter(

        follower=request.user,

        following=user_profile

    ).exists()

    return render(

        request,

        'profile.html',

        {

            'profile': profile,

            'posts': posts,

            'is_following': is_following
        }
    )

@login_required
def follow_user(request, username):

    target_user = User.objects.get(
        username=username
    )

    # PREVENT SELF FOLLOW

    if target_user != request.user:

        already_following = Follow.objects.filter(

            follower=request.user,

            following=target_user

        ).first()

        if already_following:

            already_following.delete()

        else:

            Follow.objects.create(

                follower=request.user,

                following=target_user
            )

    return redirect(
        'profile',
        username=username
    )

@login_required
def users_list(request):

    users = User.objects.exclude(
        id=request.user.id
    )

    following_users = Follow.objects.filter(

        follower=request.user

    ).values_list(

        'following_id',
        flat=True
    )

    return render(

        request,

        'users.html',

        {

            'users': users,

            'following_users': following_users
        }
    )

@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        bio = request.POST.get('bio')

        profile_image = request.POST.get(
            'profile_image'
        )

        profile.bio = bio

        profile.profile_image = profile_image

        profile.save()

        return redirect(
            'profile',
            username=request.user.username
        )

    return render(

        request,

        'edit_profile.html',

        {

            'profile': profile
        }
    )

@login_required
def edit_post(request, post_id):

    post = Post.objects.get(id=post_id)

    # SECURITY CHECK

    if post.user != request.user:

        return redirect('home')

    if request.method == 'POST':

        post.content = request.POST.get(
            'content'
        )

        post.image = request.POST.get(
            'image'
        )

        post.save()

        return redirect('home')

    return render(

        request,

        'app/edit_post.html',

        {

            'post': post
        }
    )