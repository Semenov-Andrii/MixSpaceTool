import os
import shutil

from django.core.files.base import ContentFile, File
from django.http import JsonResponse, FileResponse
from rest_framework import status, generics
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView, \
    RetrieveDestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

from app.models.repository import FileModel, Repository, Version, RepositoryMember
from app.models.user import UserProfile
from app.permitions.repository import can_access_repo, RepositoryAccessor
from app.serializers.repository_serializer import FileUploadSerializer, RepositoryListSerializer, RepositorySerializer, \
    RepositoryInfoSerializer, FileCreateSerializer, VersionSerializer, FileUpdateSerializer, RepositoryMemberSerializer
from app.serializers.user_serializer import UserProfileInfoSerializer
from app.utility import get_media_root, get_repository_root, get_media


class RepositoryCreateView(generics.CreateAPIView):
    serializer_class = RepositorySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        version = Version.objects.create(member=request.user.userprofile)
        repo = Repository.objects.create(icon=serializer.data["icon"], title=serializer.data["title"],
                                         description=serializer.data["description"],
                                         owner=self.request.user.userprofile, version=version)

        res_serializer = RepositoryListSerializer(repo)
        return JsonResponse(res_serializer.data, status=status.HTTP_200_OK)


class RepositoryRetrieveDestroyView(generics.RetrieveDestroyAPIView, RepositoryAccessor):
    serializer_class = RepositoryInfoSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        err = self.check_access(request, self.kwargs)
        if err is not None:
            return JsonResponse({"detail": err}, status=status.HTTP_400_BAD_REQUEST)
        instance = self.repository

        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        err = self.check_access(request, self.kwargs)
        if err is not None:
            return JsonResponse({"detail": err}, status=status.HTTP_400_BAD_REQUEST)
        instance = self.repository

        user_profile = self.request.user.userprofile
        if instance.owner.id != user_profile.id:
            return JsonResponse({"detail": "You can't access this repository!"}, status=status.HTTP_400_BAD_REQUEST)

        repo_path = get_repository_root(instance)
        instance.delete()

        shutil.rmtree(os.path.join(get_media(), repo_path))

        return JsonResponse({"detail": "Deleted successfully"}, status=status.HTTP_200_OK)


class OwnRepositoryListView(generics.ListAPIView):
    serializer_class = RepositoryListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_profile = self.request.user.userprofile
        return Repository.objects.filter(owner=user_profile)


class RepositoryListView(generics.ListAPIView):
    serializer_class = RepositoryListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_profile = self.request.user.userprofile
        members = RepositoryMember.objects.filter(member_id=user_profile.id)
        return [member.repository for member in members]


class FileUploadAPIView(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        res = FileModel(**serializer.validated_data)
        repository = res.repository
        if not can_access_repo(request, repository):
            return JsonResponse({"detail": "You can't access this repository"}, status=status.HTTP_400_BAD_REQUEST)

        res.file.name = res.name
        res.save()

        serializer = FileCreateSerializer(res)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)


class FileCreateAPIView(CreateAPIView):
    serializer_class = FileCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        res = FileModel(**serializer.validated_data)
        repository = res.repository

        if not can_access_repo(request, repository):
            return JsonResponse({"detail": "You can't access this repository"}, status=status.HTTP_400_BAD_REQUEST)
        res.save()
        if res.file_type == "file":
            res.file.name = res.name
            res.file.save(res.name, ContentFile(""))

        serializer = FileCreateSerializer(res)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)


class FileUpdateAPIView(UpdateAPIView):
    serializer_class = FileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file_id = self.kwargs.get("file_id")
        res = FileModel.objects.filter(id=file_id).first()
        if res is None:
            return JsonResponse({"detail": "File not found!"}, status=status.HTTP_404_NOT_FOUND)

        repository = res.repository

        if not can_access_repo(request, repository):
            return JsonResponse({"detail": "You can't access this repository"}, status=status.HTTP_400_BAD_REQUEST)

        if "content" in serializer.validated_data:
            if res.file:
                res.file.delete(save=False)

            content_file = ContentFile(serializer.validated_data["content"].encode("utf-8"), name=res.file.name)
            res.file.save(res.name, content_file, save=True)

        if "name" in serializer.validated_data:
            res.rename(serializer.validated_data["name"])

        serializer = FileCreateSerializer(res)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)


def create_file_models(repository, base_path, parent=None):
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)

        if os.path.isdir(item_path):

            folder_model = FileModel.objects.create(
                name=item,
                file_type="dir",
                parent=parent,
                repository=repository
            )

            create_file_models(repository, item_path, parent=folder_model)
        else:
            with open(item_path, "rb") as f:
                file_content = File(f, name=item)
                FileModel.objects.create(
                    name=item,
                    file_type="file",
                    parent=parent,
                    repository=repository,
                    file=file_content
                )


class VersionDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        version_id = self.kwargs.get("version_id")
        repository_id = self.kwargs.get("repository_id")
        if not version_id or not repository_id:
            return JsonResponse({"detail": "Version not found!"}, status=status.HTTP_404_NOT_FOUND)

        version = Version.objects.filter(id=version_id).first()
        repository = Repository.objects.filter(id=repository_id).first()
        if not version or not repository:
            return JsonResponse({"detail": "Version not found!"}, status=status.HTTP_404_NOT_FOUND)

        if not can_access_repo(request, repository):
            return JsonResponse({"detail": "You can't access this repository"}, status=status.HTTP_400_BAD_REQUEST)

        current = repository.version
        while current != version:
            item = current
            current = current.parent
            shutil.rmtree(get_media_root(repository, item))

        repository.version = Version.objects.create(parent=version, member=request.user.userprofile)
        repository.save()

        FileModel.objects.filter(repository_id=repository_id).delete()

        from_path = get_media_root(repository, version)

        create_file_models(repository, from_path)

        serializer = RepositoryInfoSerializer(repository)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK)


class VersionCreateAPIView(CreateAPIView, RepositoryAccessor):
    serializer_class = VersionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        err = self.check_access(request, self.kwargs)
        if err is not None:
            return JsonResponse({"detail": err}, status=status.HTTP_400_BAD_REQUEST)
        repository = self.repository

        if repository.version is None:
            repository.version = Version.objects.create()

        res = Version(**serializer.validated_data)
        res.member = request.user.userprofile
        res.parent = repository.version.parent
        res.save()

        repository.version.parent = res
        repository.version.save()

        from_path = get_media_root(repository, repository.version)
        to_path = get_media_root(repository, res)
        shutil.copytree(from_path, to_path)

        serializer = VersionSerializer(res)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)


class VersionListAPIView(ListAPIView, RepositoryAccessor):
    serializer_class = VersionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        repository_id = self.kwargs.get("repository_id")
        repository = Repository.objects.filter(id=repository_id).first()

        versions = []
        version = repository.version
        while version.parent is not None:
            versions.append(version.id)
            version = version.parent

        return Version.objects.filter(version__in=versions).order_by("-created")

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        err = self.check_access(request, self.kwargs)
        if err is not None:
            return JsonResponse({"detail": err}, status=status.HTTP_400_BAD_REQUEST)

        versions = self.get_queryset()
        serializer = VersionSerializer(versions, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


class FileRetrieveAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        file_id = self.kwargs.get("file_id")
        return FileModel.objects.filter(id=file_id)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return JsonResponse({"detail": "File not found!"}, status=status.HTTP_404_NOT_FOUND)

        instance = queryset.first()

        if not can_access_repo(self.request, instance.repository):
            return JsonResponse({"detail": "You can't access this file!"}, status=status.HTTP_400_BAD_REQUEST)

        response = FileResponse(instance.file.open("rb"), as_attachment=True, filename=instance.file.name)

        return response

class FileDestroyAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        file_id = self.kwargs.get("file_id")
        return FileModel.objects.filter(id=file_id)

    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return JsonResponse({"detail": "File not found!"}, status=status.HTTP_404_NOT_FOUND)

        instance = queryset.first()

        if not can_access_repo(self.request, instance.repository):
            return JsonResponse({"detail": "You can't access this file!"}, status=status.HTTP_400_BAD_REQUEST)

        instance.delete()

        return JsonResponse({"detail": "File removed successfully!"}, status=status.HTTP_200_OK)

class RepositoryMemberCreateView(generics.CreateAPIView):
    serializer_class = RepositoryMemberSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = UserProfile.objects.filter(user__username=serializer.data["email"]).first()
        if not user:
            return JsonResponse({"detail": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

        members = RepositoryMember.objects.filter(member=user,
                                                  repository_id=serializer.data["repositoryId"])
        if members.exists():
            return JsonResponse({"detail": "User already was added!"}, status=status.HTTP_400_BAD_REQUEST)

        user_profile = self.request.user.userprofile

        repository = Repository.objects.filter(id=serializer.data["repositoryId"], owner=user_profile).first()
        if not repository:
            return JsonResponse({"detail": "Repository not found!"}, status=status.HTTP_404_NOT_FOUND)

        if user_profile.id == user.id:
            return JsonResponse({"detail": "User already was added!"}, status=status.HTTP_400_BAD_REQUEST)

        RepositoryMember.objects.create(repository=repository, member=user)

        res_serializer = UserProfileInfoSerializer(user)
        return JsonResponse(res_serializer.data, status=status.HTTP_200_OK)


class RepositoryMemberListView(generics.ListAPIView):
    serializer_class = UserProfileInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        repository_id = self.kwargs.get("repository_id")
        members = RepositoryMember.objects.filter(repository_id=repository_id)
        repository = Repository.objects.filter(id=repository_id).first()

        return ([repository.owner] if repository else []) + [member.member for member in members]


class RepositoryMemberDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        member_id = self.kwargs.get("member_id")
        repository_id = self.kwargs.get("repository_id")
        return RepositoryMember.objects.filter(member_id=member_id, repository_id=repository_id)

    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return JsonResponse({"detail": "Member not found!"}, status=status.HTTP_404_NOT_FOUND)

        instance = queryset.first()
        user_profile = self.request.user.userprofile

        if user_profile.id != instance.repository.owner.id:
            return JsonResponse({"detail": "You can't access this repository!"}, status=status.HTTP_400_BAD_REQUEST)
        instance.delete()

        return JsonResponse({"detail": "Deleted successfully"}, status=status.HTTP_200_OK)
