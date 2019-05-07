from django.db import models

from users.models import User

from .constants import (POST_CONTENT_FIELD_MAX_LENGTH,
                        COMMENT_FIELD_MAX_LENGTH,
                        POST_TITLE_FIELD_MAX_LENGTH)


class Post(models.Model):
    title = models.CharField(max_length=POST_TITLE_FIELD_MAX_LENGTH, unique=True)
    content = models.TextField(max_length=POST_CONTENT_FIELD_MAX_LENGTH)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    posted_on = models.DateTimeField(auto_now_add=True)
    last_modified_on = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    commented_on = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=COMMENT_FIELD_MAX_LENGTH)
