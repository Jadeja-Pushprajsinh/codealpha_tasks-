from django.db import models

from django.contrib.auth.models import User


# PROJECTS

class Project(models.Model):

    name = models.CharField(
        max_length=200
    )

    description = models.TextField()

    created_by = models.ForeignKey(

        User,

        on_delete=models.CASCADE
    )

    members = models.ManyToManyField(

        User,

        related_name='projects'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    leader = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='led_projects',
        null=True,
        blank=True
    )
    def __str__(self):

        return self.name



# TASKS

class Task(models.Model):

    STATUS_CHOICES = [

        ('TODO', 'To Do'),

        ('IN_PROGRESS', 'In Progress'),

        ('DONE', 'Done'),
    ]

    project = models.ForeignKey(

        Project,

        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    assigned_to = models.ForeignKey(

        User,

        on_delete=models.SET_NULL,

        null=True,

        blank=True
    )

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='TODO'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.title


# COMMENTS

class Comment(models.Model):

    task = models.ForeignKey(

        Task,

        on_delete=models.CASCADE
    )

    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.user.username   
