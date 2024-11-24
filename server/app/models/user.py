import uuid

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255, default="Andrii Semenov")
    position = models.CharField(max_length=50, default="developer")
    avatar = models.CharField(max_length=100, default="")
