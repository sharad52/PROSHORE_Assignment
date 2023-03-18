from rest_framework import serializers
from contents.models import Content


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        field = '__all__'