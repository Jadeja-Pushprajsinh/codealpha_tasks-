from django.shortcuts import render

from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required

from .models import *
 
def register(request):

    form = UserCreationForm()

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('login')

    return render(

        request,

        'register.html',

        {

            'form': form
        }
    )


# DASHBOARD

@login_required
def dashboard(request):

    projects = Project.objects.filter(

        members=request.user

    )

    return render(

        request,

        'dashboard.html',

        {

            'projects': projects
        }
    )

@login_required
def create_project(request):

    if request.method == 'POST':

        name = request.POST.get('name')

        description = request.POST.get(
            'description'
        )

        members_input = request.POST.get(
            'members'
        )

        # CREATE PROJECT

        project = Project.objects.create(

            name=name,

            description=description,

            created_by=request.user
        )

        # ADD CREATOR

        project.members.add(request.user)

        # ADD OTHER MEMBERS

        if members_input:

            usernames = members_input.split(',')

            for username in usernames:

                username = username.strip()

                try:

                    user = User.objects.get(
                        username=username
                    )

                    project.members.add(user)

                except User.DoesNotExist:

                    pass

        return redirect('dashboard')

    return render(

        request,

        'create_project.html'
    )