from django.contrib.auth.decorators import login_required
from django.urls import path
from base.utils import anonymous_required
from .apps import UserAppConfig
from . import views
from . import constants


app_name = UserAppConfig.name


urlpatterns = [
    path(constants.SIGNUP_PATH,
         anonymous_required(views.SignUpView.as_view()),
         name=constants.SIGNUP_VIEW_NAME),

    path(constants.LOGIN_PATH,
         anonymous_required(views.LoginView.as_view()),
         name=constants.LOGIN_VIEW_NAME),

    path(constants.PROFILE_DETAILS_PATH,
         login_required(views.ProfileDetailView.as_view()),
         name=constants.PROFILE_DETAILS_VIEW_NAME),

    path(constants.PROFILE_UPDATE_PATH,
         login_required(views.ProfileUpdateView.as_view()),
         name=constants.PROFILE_UPDATE_VIEW_NAME),

    path(constants.PROFILE_PASSWORD_CHANGE_PATH,
         login_required(views.PasswordChangeView.as_view()),
         name=constants.PROFILE_PASSWORD_CHANGE_VIEW_NAME),

    path(constants.LOGOUT_PATH,
         login_required(views.LogoutView.as_view()),
         name=constants.LOGOUT_VIEW_NAME)
]
