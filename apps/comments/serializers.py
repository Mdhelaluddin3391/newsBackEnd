from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(
        source="user.full_name",
        read_only=True
    )

    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "article",
            "user_name",
            "parent",
            "content",
            "edit_count",
            "is_reported",
            "created_at",
            "replies",
        )
        read_only_fields = (
            "edit_count",
            "is_reported",
            "created_at",
        )

    def get_replies(self, obj):
        qs = obj.replies.filter(is_deleted=False)
        return CommentSerializer(qs, many=True).data
