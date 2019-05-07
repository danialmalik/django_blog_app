from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1.blogs_api.views import PostViewSet, CommentViewSet

from .apps import BlogsApiConfig
from . import constants


app_name = BlogsApiConfig.name


posts_router = DefaultRouter()
posts_router.register('', PostViewSet,
                      base_name=constants.POST_VIEW_SET_NAME)

comments_router = DefaultRouter()
comments_router.register('', CommentViewSet,
                         base_name=constants.COMMENT_VIEW_SET_NAME)

urlpatterns = [

    path(constants.POSTS_PATH,
         include(posts_router.urls)),

    path(constants.COMMENTS_PATH,
         include(comments_router.urls)),
]
