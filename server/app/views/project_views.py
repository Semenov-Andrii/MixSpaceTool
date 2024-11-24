from django.utils import timezone
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from app.models.project import Project, ProjectMember, TaskList, Task, TaskLabel, ProjectTimer
from app.models.user import UserProfile
from app.permitions.project import can_access_project, IsProjectMember, can_access_task_list, can_access_task, \
    IsProjectOwner
from app.serializers.project_serializer import ProjectSerializer, ProjectListSerializer, ProjectMemberSerializer, \
    ProjectInfoSerializer, TaskListSerializer, TaskSerializer, TaskLabelSerializer, ProjectTimerSerializer, \
    CommentSerializer
from app.serializers.user_serializer import UserProfileInfoSerializer



class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        project = Project.objects.create(icon=serializer.data["icon"], title=serializer.data["title"],
                                         description=serializer.data["description"],
                                         owner=self.request.user.userprofile)

        res_serializer = ProjectListSerializer(project)
        return JsonResponse(res_serializer.data, status=status.HTTP_200_OK)


class OwnProjectListView(generics.ListAPIView):
    serializer_class = ProjectListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_profile = self.request.user.userprofile
        return Project.objects.filter(owner=user_profile)


class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_profile = self.request.user.userprofile
        members = ProjectMember.objects.filter(member_id=user_profile.id)
        return [member.project for member in members]


class ProjectRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    serializer_class = ProjectInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        return Project.objects.filter(id=project_id)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return JsonResponse({"detail": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)

        instance = queryset.first()

        if not can_access_project(self.request, instance):
            return JsonResponse({"detail": "You can't access this project!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return JsonResponse({"detail": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)

        instance = queryset.first()

        user_profile = self.request.user.userprofile
        if instance.owner.id != user_profile.id:
            return JsonResponse({"detail": "You can't access this project!"}, status=status.HTTP_400_BAD_REQUEST)

        instance.delete()

        return JsonResponse({"detail": "Deleted successfully"}, status=status.HTTP_200_OK)

class ProjectTimerCreateView(generics.CreateAPIView):
    serializer_class = ProjectTimerSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        project_id = self.kwargs.get("project_id")
        project = Project.objects.filter(id=project_id).first()
        if not project:
            return JsonResponse({"detail": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)

        if not can_access_project(self.request, project):
            return JsonResponse({"detail": "You can't access this project!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(member=request.user.userprofile, project=project)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

class ProjectTimerEndView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        timer_id = self.kwargs.get("timer_id")
        timer = ProjectTimer.objects.filter(id=timer_id).first()
        if not timer:
            return JsonResponse({"detail": "Project timer not found!"}, status=status.HTTP_404_NOT_FOUND)

        if not can_access_project(self.request, timer.project):
            return JsonResponse({"detail": "You can't access this project!"}, status=status.HTTP_400_BAD_REQUEST)

        timer.end_time = timezone.now()
        timer.save()

        serializer = ProjectTimerSerializer(instance=timer)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

class ProjectTimerCommentView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def update(self, request, *args, **kwargs):
        timer_id = self.kwargs.get("timer_id")
        timer = ProjectTimer.objects.filter(id=timer_id).first()
        if not timer:
            return JsonResponse({"detail": "Project timer not found!"}, status=status.HTTP_404_NOT_FOUND)

        if not can_access_project(self.request, timer.project):
            return JsonResponse({"detail": "You can't access this project!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        timer.comment = serializer.data["comment"]
        timer.save()

        serializer = ProjectTimerSerializer(instance=timer)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

class ProjectTimerListView(generics.ListAPIView):
    serializer_class = ProjectTimerSerializer
    permission_classes = [IsProjectOwner]

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        return ProjectTimer.objects.filter(project_id=project_id).order_by("-id")


class MemberProjectTimerListView(generics.ListAPIView):
    serializer_class = ProjectTimerSerializer
    permission_classes = [IsProjectMember]

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        return (ProjectTimer.objects.filter(project_id=project_id, member=self.request.user.userprofile)
                .order_by("-id"))


class TaskListCreateView(generics.CreateAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        project_id = self.kwargs.get("project_id")
        project = Project.objects.filter(id=project_id).first()
        if not project:
            return JsonResponse({"detail": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)

        if not can_access_project(self.request, project):
            return JsonResponse({"detail": "You can't access this project!"}, status=status.HTTP_400_BAD_REQUEST)

        task_list = TaskList.objects.create(project=project, title=serializer.data["title"])

        serializer = self.get_serializer(task_list)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        task_list_id = self.kwargs.get("task_list_id")
        task_list: TaskList = TaskList.objects.filter(id=task_list_id).first()
        if not task_list:
            return JsonResponse({"detail": "Task list not found!"}, status=status.HTTP_404_NOT_FOUND)

        if not can_access_task_list(self.request, task_list):
            return JsonResponse({"detail": "You can't access this project!"}, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.data

        label_data = data.get("label", None)
        label = None
        if label_data:
            project_id = task_list.project_id
            label = TaskLabel.objects.filter(text=label_data["text"], project_id=project_id).first()
            if not label:
                label = TaskLabel.objects.create(text=label_data["text"], color=label_data["color"],
                                                 project_id=project_id)
            else:
                label.color = label_data["color"]
                label.save()

        member_data = data.get("member", None)

        member = None
        if member_data:
            member = UserProfile.objects.filter(user__username=member_data["email"]).first()

        task = Task.objects.create(task_list=task_list, title=data["title"], description=data["description"],
                                   is_done=data["isDone"], label=label, member=member)

        serializer = self.get_serializer(task)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)


class TaskUpdateView(generics.UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()

    def update(self, request, *args, **kwargs):
        instance: Task = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if not can_access_task(self.request, instance):
            return JsonResponse({"detail": "You can't access this project!"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)

        data = serializer.data
        label_data = data.get("label", None)
        label = None
        if label_data:
            project_id = instance.task_list.project_id
            label = TaskLabel.objects.filter(text=label_data["text"], project_id=project_id).first()
            if not label:
                label = TaskLabel.objects.create(text=label_data["text"], color=label_data["color"],
                                                 project_id=project_id)
            else:
                label.color = label_data["color"]
                label.save()

        member_data = data.get("member", None)

        member = None
        if member_data:
            member = UserProfile.objects.filter(user__username=member_data["email"]).first()

        instance.label = label
        instance.member = member
        instance.title = serializer.data["title"]
        instance.description = serializer.data["description"]
        instance.is_done = serializer.data["isDone"]
        instance.save()

        serializer = self.get_serializer(instance)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK)


class TaskLabelListView(generics.ListAPIView):
    serializer_class = TaskLabelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        return TaskLabel.objects.filter(project_id=project_id)


class TaskDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs.get("task_id")
        return Task.objects.filter(id=task_id)

    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return JsonResponse({"detail": "Task not found!"}, status=status.HTTP_404_NOT_FOUND)

        instance = queryset.first()

        if not can_access_task(self.request, instance):
            return JsonResponse({"detail": "You can't access this project!"}, status=status.HTTP_400_BAD_REQUEST)

        instance.delete()

        return JsonResponse({"detail": "Deleted successfully"}, status=status.HTTP_200_OK)


class TaskListDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task_list_id = self.kwargs.get("task_list_id")
        return TaskList.objects.filter(id=task_list_id)

    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return JsonResponse({"detail": "Task list not found!"}, status=status.HTTP_404_NOT_FOUND)

        instance = queryset.first()

        if not can_access_task_list(self.request, instance):
            return JsonResponse({"detail": "You can't access this project!"}, status=status.HTTP_400_BAD_REQUEST)
        instance.delete()

        return JsonResponse({"detail": "Deleted successfully"}, status=status.HTTP_200_OK)


class ProjectMemberCreateView(generics.CreateAPIView):
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = UserProfile.objects.filter(user__username=serializer.data["email"]).first()
        if not user:
            return JsonResponse({"detail": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

        members = ProjectMember.objects.filter(member=user,
                                               project_id=serializer.data["projectId"])
        if members.exists():
            return JsonResponse({"detail": "User already was added!"}, status=status.HTTP_400_BAD_REQUEST)

        user_profile = self.request.user.userprofile

        project = Project.objects.filter(id=serializer.data["projectId"], owner=user_profile).first()
        if not project:
            return JsonResponse({"detail": "Project not found!"}, status=status.HTTP_404_NOT_FOUND)

        if user_profile.id == user.id:
            return JsonResponse({"detail": "User already was added!"}, status=status.HTTP_400_BAD_REQUEST)

        ProjectMember.objects.create(project=project, member=user)

        res_serializer = UserProfileInfoSerializer(user)
        return JsonResponse(res_serializer.data, status=status.HTTP_200_OK)


class ProjectMemberListView(generics.ListAPIView):
    serializer_class = UserProfileInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        members = ProjectMember.objects.filter(project_id=project_id)
        project = Project.objects.filter(id=project_id).first()

        return ([project.owner] if project else []) + [member.member for member in members]


class ProjectMemberDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member_id = self.kwargs.get("member_id")
        project_id = self.kwargs.get("project_id")
        return ProjectMember.objects.filter(member_id=member_id, project_id=project_id)

    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return JsonResponse({"detail": "Member not found!"}, status=status.HTTP_404_NOT_FOUND)

        instance = queryset.first()
        user_profile = self.request.user.userprofile

        if user_profile.id != instance.project.owner.id:
            return JsonResponse({"detail": "You can't access this project!"}, status=status.HTTP_400_BAD_REQUEST)
        instance.delete()

        return JsonResponse({"detail": "Deleted successfully"}, status=status.HTTP_200_OK)
