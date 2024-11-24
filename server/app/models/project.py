import uuid

from django.db import models

from app.models.user import UserProfile


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, default="", null=True)
    icon = models.CharField(max_length=100)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class TaskList(models.Model):
    title = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="task_lists")


class TaskLabel(models.Model):
    text = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Task(models.Model):
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name="tasks")

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    is_done = models.BooleanField(default=False)

    member = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, default=None)
    label = models.ForeignKey(TaskLabel, on_delete=models.SET_NULL, null=True, default=None)


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

class ProjectTimer(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)

    comment = models.TextField(default="", blank=True)
