from rest_framework import serializers

from app.models.project import Project, TaskList, Task, TaskLabel, ProjectTimer
from app.serializers.user_serializer import UserProfileInfoSerializer
from app.utility import CamelCaseModelSerializer, CamelCaseSerializer


class ProjectSerializer(CamelCaseModelSerializer):
    description = serializers.CharField(max_length=1000, allow_blank=True)

    class Meta:
        model = Project
        fields = ["title", "description", "icon"]


class TaskLabelSerializer(CamelCaseModelSerializer):
    class Meta:
        model = TaskLabel
        fields = ["text", "color"]


class TaskSerializer(CamelCaseModelSerializer):
    label = TaskLabelSerializer(required=False, allow_null=True)
    member = UserProfileInfoSerializer(required=False, allow_null=True)

    description = serializers.CharField(max_length=1000, allow_blank=True)

    class Meta:
        model = Task
        fields = ["id", "title", "description", "is_done", "label", "member"]


class TaskListSerializer(CamelCaseModelSerializer):
    tasks = TaskSerializer(many=True, required=False)
    id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = TaskList
        fields = ["id", "title", "tasks"]


class ProjectInfoSerializer(CamelCaseModelSerializer):
    task_lists = TaskListSerializer(many=True)
    owner = UserProfileInfoSerializer()

    class Meta:
        model = Project
        fields = ["id", "title", "description", "icon", "owner", "task_lists"]


class ProjectListSerializer(CamelCaseModelSerializer):
    owner = UserProfileInfoSerializer()

    class Meta:
        model = Project
        fields = ["id", "title", "description", "icon", "owner"]


class ProjectMemberSerializer(CamelCaseSerializer):
    email = serializers.EmailField()
    project_id = serializers.UUIDField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

class ProjectTimerSerializer(CamelCaseModelSerializer):
    member = UserProfileInfoSerializer(required=False, allow_null=True)
    end_time = serializers.DateTimeField(read_only=True, allow_null=True)
    comment = serializers.CharField(max_length=1000, read_only=True, required=False)

    class Meta:
        model = ProjectTimer
        fields = ["id", "member", "start_time", "end_time", "comment"]

class CommentSerializer(CamelCaseSerializer):
    comment = serializers.CharField(max_length=1000, allow_blank=True)