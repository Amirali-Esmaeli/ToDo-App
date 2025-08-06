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

    def create(self, validated_data):
        user = self.context["request"].user
        if not user.is_verified:
            raise serializers.ValidationError(
                "Only verified users can create tasks."
            )
        validated_data["user"] = user
        return super().create(validated_data)
