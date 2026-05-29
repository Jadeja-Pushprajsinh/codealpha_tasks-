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

        leader_username = request.POST.get(
            'leader'
        )

        # GET LEADER

        try:

            leader = User.objects.get(
                username=leader_username
            )

        except User.DoesNotExist:

            leader = request.user

        # CREATE PROJECT

        project = Project.objects.create(

            name=name,

            description=description,

            created_by=request.user,

            leader=leader
        )

        # ADD CREATOR

        project.members.add(request.user)

        # MEMBER USERNAMES

        member_fields = [

            'member1',

            'member2',

            'member3',

            'member4',

            'member5'
        ]

        for field in member_fields:

            username = request.POST.get(field)

            if username:

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

@login_required
def project_board(request, project_id):

    project = Project.objects.get(
        id=project_id
    )

    todo_tasks = Task.objects.filter(

        project=project,

        status='TODO'
    )

    in_progress_tasks = Task.objects.filter(

        project=project,

        status='IN_PROGRESS'
    )

    done_tasks = Task.objects.filter(

        project=project,

        status='DONE'
    )

    return render(

        request,

        'project_board.html',

        {

            'project': project,

            'todo_tasks': todo_tasks,

            'in_progress_tasks': in_progress_tasks,

            'done_tasks': done_tasks
        }
    )

@login_required
def create_task(request, project_id):

    project = Project.objects.get(
        id=project_id
    )

    if request.method == 'POST':

        title = request.POST.get(
            'title'
        )

        description = request.POST.get(
            'description'
        )

        assigned_username = request.POST.get(
            'assigned_to'
        )

        try:

            assigned_user = User.objects.get(
                username=assigned_username
            )

        except User.DoesNotExist:

            assigned_user = None

        Task.objects.create(

            project=project,

            title=title,

            description=description,

            assigned_to=assigned_user,

            status='TODO'
        )

        return redirect(
            'project_board',
            project_id=project.id
        )

    return render(

        request,

        'create_task.html',

        {

            'project': project
        }
    )