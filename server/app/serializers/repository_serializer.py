from rest_framework import serializers

from app.models.repository import FileModel, Repository, Version
from app.serializers.user_serializer import UserProfileInfoSerializer
from app.utility import CamelCaseModelSerializer, CamelCaseSerializer


class RepositorySerializer(CamelCaseModelSerializer):
    description = serializers.CharField(max_length=1000, allow_blank=True)

    class Meta:
        model = Repository
        fields = ["title", "description", "icon"]


class RepositoryListSerializer(CamelCaseModelSerializer):
    owner = UserProfileInfoSerializer()

    class Meta:
        model = Repository
        fields = ["id", "title", "description", "icon", "owner", "version"]


class FileUploadSerializer(CamelCaseModelSerializer):
    class Meta:
        model = FileModel
        fields = ["id", "file", "parent", "repository", "name"]


class FileCreateSerializer(CamelCaseModelSerializer):
    files = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = FileModel
        fields = ["id", "parent", "name", "file_type", "repository", "files"]

    def get_files(self, obj):
        files = obj.files.all()
        return FileCreateSerializer(files, many=True, context={"obj_instance": obj}).data

    def serialize_entity_child(self, entity_instance):
        if "obj_instance" in self.context:
            entity_child_instance = entity_instance.files.filter(
                id=self.context["obj_instance"].id).first()
            if entity_child_instance:
                return FileCreateSerializer(entity_child_instance).data
        return {}

    def to_representation(self, instance):
        rep = super(FileCreateSerializer, self).to_representation(instance)
        return {**rep, **self.serialize_entity_child(instance)}


class FileUpdateSerializer(CamelCaseSerializer):
    content = serializers.CharField(allow_blank=True, required=False)
    name = serializers.CharField(allow_blank=True, required=False)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class VersionSerializer(CamelCaseModelSerializer):
    member = UserProfileInfoSerializer(read_only=True)

    class Meta:
        model = Version
        fields = ["id", "title", "created", "member"]


class RepositoryInfoSerializer(CamelCaseModelSerializer):
    files = serializers.SerializerMethodField(required=False, allow_null=True)
    versions = serializers.SerializerMethodField(required=False, allow_null=True)
    owner = UserProfileInfoSerializer()

    class Meta:
        model = Repository
        fields = ["id", "title", "description", "icon", "owner", "files", "versions"]

    def get_files(self, obj):
        files = FileModel.objects.filter(repository=obj, parent=None).all()
        return FileCreateSerializer(instance=files, many=True).data

    def get_versions(self, obj):
        versions = []
        version = obj.version
        while version is not None:
            versions.append(version)
            version = version.parent

        return VersionSerializer(instance=versions, many=True).data


class RepositoryMemberSerializer(CamelCaseSerializer):
    email = serializers.EmailField()
    repository_id = serializers.UUIDField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
