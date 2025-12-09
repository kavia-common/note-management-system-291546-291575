from rest_framework import serializers
from .models import Note


# PUBLIC_INTERFACE
class NoteSerializer(serializers.ModelSerializer):
    """Serializer for the Note model providing validation and JSON representation."""

    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_title(self, value: str) -> str:
        """Ensure title is not empty or only whitespace."""
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()
