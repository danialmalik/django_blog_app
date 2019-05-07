from django.contrib.auth import password_validation, update_session_auth_hash
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import Profile, User
from users.constants import PASSWORD_FIELD_MAX_LENGTH, DEFAULT_PROFILE_PICTURE, \
    PROFILE_PICTURES_DIR

DEFAULT_PROFILE_PICTURE_PATH = '{}{}'.format(PROFILE_PICTURES_DIR, DEFAULT_PROFILE_PICTURE)


class UserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=PASSWORD_FIELD_MAX_LENGTH,
                                      write_only=True,
                                      required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate_password2(self, password2):
        initial = self.get_initial()
        password1 = initial.get('password')
        if password1 != password2:
            raise ValidationError('Password do not match')
        return password2

    def validate(self, attrs):
        # if password2 field is in data then remove it. we do not need it for creating user.
        if 'password2' in attrs:
            del attrs['password2']
        user = User(**attrs)

        password = attrs.get('password')

        errors = {}  # a dict for getting the password field errors in list with key 'password1'

        try:
            password_validation.validate_password(password, user=user)
        except DjangoValidationError as e:
            # Here the 'ValidationError' raised is from django exceptions
            errors['password2'] = list(e.messages)
            raise ValidationError(errors)

        return super(UserCreateSerializer, self).validate(attrs)

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

        extra_kwargs = {
            'username': {
                'validators': []  # otherwise "user already exists" exception occurs
            },
            'password': {
                'write_only': True  # password is not returned
            }
        }


class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=PASSWORD_FIELD_MAX_LENGTH)
    new_password1 = serializers.CharField(max_length=PASSWORD_FIELD_MAX_LENGTH)
    new_password2 = serializers.CharField(max_length=PASSWORD_FIELD_MAX_LENGTH)

    def get_request(self):
        return self.context.get('request')

    def validate_old_password(self, old_password):
        user = self.get_request().user
        if user.check_password(old_password):
            return old_password
        raise ValidationError('incorrect old password')

    def validate_new_password1(self, new_password1):
        try:
            password_validation.validate_password(new_password1,
                                                  user=self.get_request().user)
            return new_password1

        except DjangoValidationError as exception:
            # Here the 'ValidationError' raised is from django exceptions
            raise ValidationError(list(exception.messages))

    def validate_new_password2(self, new_password2):
        initial = self.get_initial()
        new_password1 = initial.get('new_password1')
        if new_password1 != new_password2:
            raise ValidationError('Passwords do not match')
        return new_password2

    def save(self, **kwargs):
        user = self.get_request().user
        user.set_password(self.validated_data['new_password1'])
        user.save()
        update_session_auth_hash(self.get_request(), user)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'date_joined')
        read_only_fields = ('date_joined',)
        extra_kwargs = {
            'username': {
                'validators': []
            }
        }


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    def validate(self, attrs):
        instance = self.instance
        user = attrs.get('user')
        if instance:  # Profile is being updated. So instance is present
            user_instance = instance.user
            errors = {}
            try:
                if user_instance.username != user.get('username'):
                    # name is being changed.
                    User.objects.get(username=user['username'])
                    errors['username'] = 'User with that username already exists.'
            except User.DoesNotExist:
                # new username does not already exist
                pass

            try:
                if user_instance.email != user.get('email'):
                    User.objects.get(email=user['email'])
                    # email is being changed
                    errors['email'] = 'User with that email already exists.'
            except User.DoesNotExist:
                # new email does not already exist
                pass

            if errors:
                raise ValidationError(errors)
        return attrs

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')

        instance.user.username = user_data.get('username', instance.user.username)
        instance.user.email = user_data.get('email', instance.user.email)
        instance.user.first_name = user_data.get('first_name', instance.user.first_name)
        instance.user.last_name = user_data.get('last_name', instance.user.last_name)
        instance.user.save()

        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.address = validated_data.get('address', instance.address)
        instance.profile_picture = validated_data.get('profile_picture',
                                                      DEFAULT_PROFILE_PICTURE_PATH)
        instance.save()
        return instance

    class Meta:
        model = Profile
        fields = '__all__'
