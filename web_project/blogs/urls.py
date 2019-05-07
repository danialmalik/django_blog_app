from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views
from . import constants


app_name = constants.APP_NAME


urlpatterns = [
    path(constants.INDEX_PATH,
         views.Index.as_view(),
         name=constants.INDEX_VIEW_NAME),
    path(constants.POSTS_LIST_PATH,
         views.PostsList.as_view(),
         name=constants.POSTS_LIST_VIEW_NAME),

    path(constants.POST_CREATE_PATH,
         login_required(views.PostCreate.as_view()),
         name=constants.POST_CREATE_VIEW_NAME),

    path(constants.MY_POSTS_PATH,
         login_required(views.MyPosts.as_view()),
         name=constants.MY_POSTS_VIEW_NAME),

    path(constants.POST_EDIT_PATH,
         login_required(views.PostEdit.as_view()),
         name=constants.POST_EDIT_VIEW_NAME),

    path(constants.POST_DELETE_PATH,
         login_required(views.PostDelete.as_view()),
         name=constants.POST_DELETE_VIEW_NAME),

    path(constants.POST_DETAILS_PATH,
         views.PostDetailsView.as_view(),
         name=constants.POST_DETAILS_VIEW_NAME)
]
