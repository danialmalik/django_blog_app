from django.contrib.auth.models import User as BaseUser
from django.db import models
from django.urls import reverse

from base.utils import not_in_future

from .constants import ADDRESS_FIELD_MAX_LENGTH, DEFAULT_PROFILE_PICTURE, PROFILE_PICTURES_DIR
from .utils import _get_upload_path


DEFAULT_PROFILE_PICTURE_PATH = '{}{}'.format(PROFILE_PICTURES_DIR,
                                             DEFAULT_PROFILE_PICTURE)


class User(BaseUser):

    def get_absolute_url(self):
        return reverse('app:profile_details', kwargs={'id': self.id})

    class Meta:
        proxy = True


class Profile(models.Model):
    profile_picture = models.ImageField(upload_to=_get_upload_path,
                                        default=DEFAULT_PROFILE_PICTURE_PATH)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True, validators=[not_in_future])
    address = models.CharField(max_length=ADDRESS_FIELD_MAX_LENGTH, null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            old_instance = Profile.objects.get(id=self.id)
            if (old_instance.profile_picture != self.profile_picture and
                    old_instance.profile_picture.name != DEFAULT_PROFILE_PICTURE_PATH):
                old_instance.profile_picture.delete(save=False)
        except Profile.DoesNotExist as ex:
            pass
        super(Profile, self).save(*args, **kwargs)
