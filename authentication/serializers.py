from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    """ This serializes registration requests and creates a new user"""
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['id', 'first_name', 'last_name', 'surname', 'password', 'reg_number', 'groups',]

    @classmethod
    def create(self, data):
        # Use the create user method we wrote earlier to create a new user
        return User.objects.create_user(**data)

class LoginSerializer(serializers.Serializer):
    """Login serializer Class"""

    reg_number = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    @staticmethod
    def validate(data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an reg_number
        # and password and that this combination matches one of the users in
        # our database.
        reg_number = data.get('reg_number', None)
        password = data.get('password', None)

        # As mentioned above, an reg_number is required. Raise an exception if an
        # reg_number is not provided.
        if reg_number is None:
            raise serializers.ValidationError(
                'An reg_number address is required to log in.'
            )

        # As mentioned above, a password is required. Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this reg_number/password combination. Notice how
        # we pass `reg_number` as the `surname` value. Remember that, in our User
        # model, we set `USERNAME_FIELD` as `reg_number`.
        user = authenticate(reg_number=reg_number, password=password)

        # If no user was found matching this reg_number/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            resp = {
                'credentials': 'Wrong svc number or password.'
            }
            raise serializers.ValidationError(resp)
        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'reg_number': user.reg_number,
            'token': user.token
        }
class UserRetriveUpdateSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""
    password = serializers.CharField(write_only=True)

    @classmethod
    def update(self, instance, validated_data):
        """Performs an update on a User."""

        # Passwords should not be handled with `setattr`, unlike other fields.
        # This is because Django provides a function that handles hashing and
        # salting passwords, which is important for security. What that means
        # here is that we need to remove the password field from the
        # `validated_data` dictionary before iterating over it.
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()` is the method mentioned above. It handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)

        # Finally, after everything has been updated, we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'surname', 'reg_number', 'password',)
