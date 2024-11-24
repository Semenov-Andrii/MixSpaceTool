from django.conf import settings
from rest_framework import serializers


def error_detail_to_error_list(validation_error):
    errors = [pair for pair in validation_error.detail.items()]
    print(errors)
    errors = [(field, item) for field, sublist in errors for item in sublist]
    print(errors)
    return [f"{field.title()}: {error.title()}" for field, error in errors]


def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def camel_to_snake(camel_str):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in camel_str]).lstrip('_')


def to_representation(super, instance):
    ret = super.to_representation(instance)
    return {snake_to_camel(key): value for key, value in ret.items()}


def to_internal_value(super, data):
    snake_case_data = {camel_to_snake(key): value for key, value in data.items()}
    return super.to_internal_value(snake_case_data)


def get_repository_root(repository):
    return f"repositories\\{repository.id}"


def get_version_root(repository, version):
    return f"{get_repository_root(repository)}\\{version.id}"


def get_media_root(repository, version):
    return f"{settings.MEDIA_ROOT}\\{get_version_root(repository, version)}"

def get_media():
    return settings.MEDIA_ROOT

def get_file_path(repository, parent):
    parent_path = ""
    while parent:
        parent_path = parent.name + "\\" + parent_path
        parent = parent.parent

    return f"{get_version_root(repository, repository.version)}\\{parent_path}"


def file_upload_to(instance, filename):
    return get_file_path(instance.repository, instance.parent) + filename


class CamelCaseModelSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        return to_representation(super(), instance)

    def to_internal_value(self, data):
        return to_internal_value(super(), data)


class CamelCaseSerializer(serializers.Serializer):

    def to_representation(self, instance):
        return to_representation(super(), instance)

    def to_internal_value(self, data):
        return to_internal_value(super(), data)
