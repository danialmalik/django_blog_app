from rest_framework import serializers

from blogs.models import Comment, Post
from users.models import User


class CommentSerializer(serializers.ModelSerializer):
    commented_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    post = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all()
    )

    def to_representation(self, instance):
        data = super(CommentSerializer, self).to_representation(instance)
        data['commented_by'] = instance.commented_by.username
        return data

    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    # to automatically set posted_by to current user, using CurrentUserDefault()
    posted_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    def to_representation(self, instance):
        data = super(PostSerializer, self).to_representation(instance)
        posted_by = instance.posted_by.username
        data['posted_by'] = posted_by
        return data

    class Meta:
        model = Post
        fields = '__all__'
