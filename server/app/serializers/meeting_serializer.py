from rest_framework import serializers

from app.models.meeting import Meeting
from app.serializers.user_serializer import UserProfileInfoSerializer
from app.utility import CamelCaseModelSerializer, CamelCaseSerializer


class MeetingSerializer(CamelCaseModelSerializer):
    class Meta:
        model = Meeting
        fields = ["icon", "title"]


class SavedMeetingSerializer(CamelCaseSerializer):
    id = serializers.UUIDField()

class InviteMeetingSerializer(CamelCaseSerializer):
    id = serializers.UUIDField()
    email = serializers.EmailField()

class MeetingListSerializer(CamelCaseModelSerializer):
    owner = UserProfileInfoSerializer()

    class Meta:
        model = Meeting
        fields = ["id", "icon", "title", "owner"]
