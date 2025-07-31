from rest_framework import serializers
from todo.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "user",
            "complete",
            "created_date",
            "updated_date",
        ]
        read_only_fields = ["user"]
