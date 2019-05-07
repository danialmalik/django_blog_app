from django.urls import path

from .apps import UsersApiConfig
from . import views
from . import constants

app_name = UsersApiConfig.name


urlpatterns = [
    path(constants.USER_LOGIN_PATH,
         views.UserLoginAPIView.as_view(),
         name=constants.USER_LOGIN_VIEW_NAME),

    path(constants.USER_REGISTER_PATH,
         views.UserCreateAPIView.as_view(),
         name=constants.USER_REGISTER_VIEW_NAME),

    path(constants.USER_LOGOUT_PATH,
         views.UserLogoutAPIView.as_view(),
         name=constants.USER_LOGOUT_VIEW_NAME),

    path(constants.USER_PASSWORD_CHANGE_PATH,
         views.UserPasswordChangeAPIView.as_view(),
         name=constants.USER_PASSWORD_CHANGE_VIEW_NAME),

    path(constants.PROFILE_PATH,
         views.UserProfileAPIView.as_view(),
         name=constants.PROFILE_VIEW_NAME),

]
