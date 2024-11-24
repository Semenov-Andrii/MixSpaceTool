import os
import shutil
import uuid

from django.db import models

from app.models.user import UserProfile
from app.utility import file_upload_to, get_media_root, get_media


class Version(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, default="uncommited")
    created = models.DateTimeField(auto_now_add=True)
    member = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    parent = models.ForeignKey("Version", null=True, blank=True, on_delete=models.CASCADE, default=None)


class Repository(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, default="", null=True)
    icon = models.CharField(max_length=100)
    version = models.ForeignKey(Version, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class FileModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(null=True, upload_to=file_upload_to, max_length=500)

    name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=100, default="file")
    created_at = models.DateTimeField(auto_now_add=True)

    parent = models.ForeignKey("FileModel", null=True, blank=True, on_delete=models.CASCADE, related_name="files")
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name="files")

    def delete(self, *args, **kwargs):
        for child in self.files.all():
            child.delete()

        if self.file:
            self.file.delete(save=False)
        else:
            root = get_media()
            path = file_upload_to(self, self.name)
            shutil.rmtree(os.path.join(root, path))

        super().delete(*args, **kwargs)

    def rename(self, new_name):
        if new_name == self.name:
            return

        if self.file:
            old_path = self.file.path
            new_path = os.path.join(os.path.dirname(old_path), new_name)

            if os.path.exists(old_path):
                os.rename(old_path, new_path)

            self.file.name = new_path
            self.name = new_name

        else:
            media = get_media_root(self.repository, self.repository.version)
            old_folder_path = os.path.join(media, self.name)
            new_folder_path = os.path.join(media, new_name)

            if os.path.exists(old_folder_path):
                os.rename(old_folder_path, new_folder_path)

            self.name = new_name
            for child in self.files.all():
                if child.file:
                    old_file_path = child.file.name
                    new_file_path = old_file_path.replace(old_folder_path, new_folder_path)

                    child.file.name = new_file_path
                    child.save()

        self.save()

class RepositoryMember(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    member = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
