from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

# Login url for app.
LOGIN_URL = settings.LOGIN_URL
LOGGED_IN_HOME = settings.LOGGED_IN_HOME


def anonymous_required(function, redirect_to=LOGGED_IN_HOME):
    """Decorator for views that checks that the user is NOT logged in, redirecting
    to the homepage if not specified.
    """
    verify_anonymous = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_to
    )
    if function:
        return verify_anonymous(function)
    return verify_anonymous


def not_in_future(value):
    """ Validates if a date is not from future"""
    today = timezone.now().date()
    if value > today:
        raise ValidationError('Birthday date cannot be in the future.')


def get_reverse_url(app_name, url_name):
    """ Return a formatted reverse url for reverse and reverse_lazy calls"""
    return '{}:{}'.format(app_name, url_name)


def get_template_path(app_name, template_name):
    """ Return a formatted template path"""
    return '{}/{}'.format(app_name, template_name)
