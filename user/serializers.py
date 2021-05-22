import typing, re
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from user.models import User


def validate_username(username):
    rule = re.compile("[a-zA-Z0-9._]*$")  # alphanumeric and underscore
    if not rule.match(username):
        raise serializers.ValidationError(
            'Username must be alphanumeric, dot and underscore(_).')


def validate_numeric(value):
    if not value.isnumeric():
        raise serializers.ValidationError('This field must be numeric.')


def validate_phone_number(value):
    error_message = 'This field must be in following format: "01012341234".'
    if len(value) != 11:
        raise serializers.ValidationError(error_message)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        min_length=5,
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            validate_username,
        ],
        max_length=30,
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[
            validate_password,
        ],
        min_length=1,
        max_length=128,
    )
    disability_grade = serializers.IntegerField(required=True,
                                                min_value=1,
                                                max_value=6)
    phone_number = serializers.CharField(validators=[validate_phone_number],
                                         min_length=11,
                                         max_length=11)

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'disability_grade',
            'name',
            'phone_number',
        )

    def create(self, data: typing.Dict):
        # create user
        user = User.objects.create(
            username=data['username'],
            password=data['password'],
            disability_grade=data['disability_grade'],
            name=data['name'],
            phone_number=data['phone_number'],
        )
        user.set_password(data['password'])
        user.save()
        return user


class UserSerializerDocument(UserSerializer):
    password = None

    class Meta(UserSerializer.Meta):
        fields = (
            'username',
            'password',
            'disability_grade',
            'name',
            'phone_number',
        )