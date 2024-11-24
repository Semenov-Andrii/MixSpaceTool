from rest_framework.permissions import IsAuthenticated

from app.models.project import Project, ProjectMember


def can_access_project(request, project):
    user_profile = request.user.userprofile
    return (project.owner.id == user_profile.id
            or ProjectMember.objects.filter(member_id=user_profile.id, project_id=project.id).exists())


def can_access_task_list(request, task_list):
    return can_access_project(request, task_list.project)


def can_access_task(request, task):
    return can_access_task_list(request, task.task_list)

class IsProjectMember(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        project_id = view.kwargs.get("project_id")
        if not project_id:
            return False

        project = Project.objects.filter(id=project_id).first()
        if not project:
            return False

        return can_access_project(request, project)

class IsProjectOwner(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        project_id = view.kwargs.get("project_id")
        if not project_id:
            return False

        project = Project.objects.filter(id=project_id).first()
        if not project:
            return False

        user_profile = request.user.userprofile
        return project.owner.id == user_profile.id
