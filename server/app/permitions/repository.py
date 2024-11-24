from rest_framework.permissions import IsAuthenticated

from app.models.repository import Repository, RepositoryMember


def can_access_repo(request, repo):
    user_profile = request.user.userprofile
    return (repo.owner.id == user_profile.id
            or RepositoryMember.objects.filter(member_id=user_profile.id, repository_id=repo.id).exists())


class RepositoryAccessor:
    def __init__(self):
        self.repository = None

    def check_access(self, request, kwargs):
        repository_id = kwargs.get("repository_id")
        if not repository_id:
            return "Repository not found!"

        self.repository = Repository.objects.filter(id=repository_id).first()
        if not self.repository:
            return "Repository not found!"

        if not can_access_repo(request, self.repository):
            return "You can't access this repository!"

        return None


class IsRepositoryMember(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        repository_id = request.query_params.get('repository_id')
        if not repository_id:
            return False

        repository = Repository.objects.filter(id=repository_id).first()
        if not repository:
            return False

        return can_access_repo(request, repository)
