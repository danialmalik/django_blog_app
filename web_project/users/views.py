from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.views.generic import DetailView
from django.views.generic.base import View
from django.shortcuts import render, redirect

from base.utils import get_template_path

from .models import User
from .forms import LoginForm, SignUpForm, ProfileForm, UserUpdateForm
from . import constants


class SignUpView(View):
    template_name = get_template_path(constants.APP_NAME,
                                      constants.SIGNUP_TEMPLATE)

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form, 'title': 'Signup'})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User Registration Successful! Login to continue')
            # return redirect(get_reverse_url(constants.APP_NAME, constants.LOGIN_PATH))
            return JsonResponse(
                {'status': 'successful'},
                status=HTTPStatus.CREATED
            )
        else:
            # return render(request, self.template_name, {'form':form})
            return JsonResponse(
                {'errors': form.errors.as_json()},
                status=HTTPStatus.BAD_REQUEST
            )


class LoginView(View):
    template_name = get_template_path(constants.APP_NAME,
                                      constants.LOGIN_TEMPLATE)
    success_url = settings.LOGIN_REDIRECT_URL

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form, 'title': 'Login'})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful')
            # return redirect(self.success_url)
            return JsonResponse(
                {'status': 'successful'},
                status=HTTPStatus.OK
            )
        # return render(request, self.template_name, {'form':form})
        return JsonResponse(
            {'errors': form.errors.as_json()},
            status=HTTPStatus.BAD_REQUEST
        )


class ProfileDetailView(DetailView):
    model = User
    template_name = get_template_path(constants.APP_NAME,
                                      constants.PROFILE_DETAILS_TEMPLATE)

    def get_object(self, queryset=None):
        return self.request.user


class LogoutView(View):
    redirect_url = settings.LOGIN_URL

    def post(self, request):
        logout(request)
        messages.success(request, 'User logged out.')
        return JsonResponse(
            {'status': 'successful'},
            status=HTTPStatus.OK
        )


class ProfileUpdateView(View):
    template_name = get_template_path(constants.APP_NAME,
                                      constants.PROFILE_UPDATE_TEMPLATE)

    def get(self, request):
        user = request.user
        profile = user.profile
        user_form = UserUpdateForm(instance=user)
        profile_form = ProfileForm(instance=profile)
        return render(request, self.template_name,
                      {
                          'user_form': user_form,
                          'profile_form': profile_form
                      })

    def post(self, request):
        user = request.user
        user_form = UserUpdateForm(data=request.POST, instance=user)
        profile_form = ProfileForm(data=request.POST, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile Updated!')
            # return redirect(get_reverse_url(constants.APP_NAME,constants.PROFILE_DETAILS_PATH))
            return JsonResponse(
                {'status': 'successful'}
            )
        else:
            errors = user_form.errors
            errors.update(profile_form.errors)
            # return render(request, self.template_name,{
            #               'user_form': user_form,
            #               'profile_form': profile_form
            #           })
            return JsonResponse(
                {'errors': errors.as_json()},
                status=HTTPStatus.BAD_REQUEST
            )


class PasswordChangeView(View):
    template_name = get_template_path(constants.APP_NAME,
                                      constants.PROFILE_PASSWORD_CHANGE_TEMPLATE)

    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request=request,
                      template_name=self.template_name,
                      context={'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # update session hash
            messages.success(request, 'Your password was successfully updated!')
            # return redirect(get_reverse_url(constants.APP_NAME,constants.PROFILE_DETAILS_PATH))
            return JsonResponse(
                {'status': 'successful'}
            )
        else:
            # return render(request, self.template_name, {'form':form})
            return JsonResponse(
                {'status': 'failed',
                 'errors': form.errors.as_json()},
                status=HTTPStatus.BAD_REQUEST
            )
