from django.utils import timezone

from .constants import PROFILE_PICTURES_DIR


def _get_upload_path(instance, filename):
    """Generate filename as current datetime for profile picture being uploaded"""
    path = PROFILE_PICTURES_DIR
    filename = str(instance.user.id) + str(timezone.now()) + '.img'
    return path + filename
