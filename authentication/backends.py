import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User

"""Configure JWT Here"""


class JWTAuthentication(authentication.BaseAuthentication):
    """
    This class will handle users' authentication
    """

    def authenticate(self, request):
        """
        This method will authenticate the authorization headers provided.
        It is called regardless of whether the endpoint requires 
        authentication. 
        """
        prefix = 'Bearer'
        header = authentication.get_authorization_header(request).split()

        if not header:
            return None

        if len(header) < 2:
            resp = 'The authorization header provided is invalid!'
            raise exceptions.AuthenticationFailed(resp)

        if header[0].decode('utf-8') != prefix:
            resp = 'Please use a Bearer token!'
            raise exceptions.AuthenticationFailed(resp)

        token = header[1].decode('utf-8')

        return self.authenticate_token(request, token)

    def authenticate_token(self, request, token):
        """
        This method will authenticate the provided token
        """
        try:
            payload = jwt.api_jwt.decode(
                token, settings.SECRET_KEY, algorithms='HS256')
        except jwt.api_jwt.DecodeError:
            resp = 'Invalid Token. The token provided cannot be decoded!'
            raise exceptions.AuthenticationFailed(resp)
        except jwt.api_jwt.ExpiredSignatureError:
            resp = 'The token used has expired. Please authenticate again!'
            raise exceptions.AuthenticationFailed(resp)

        reg_number = payload['user_data']['reg_number']
        surname = payload['user_data']['surname']

        try:
            user = User.objects.get(reg_number=reg_number, surname=surname)
        except User.DoesNotExist:
            resp = 'No user was found from the provided token!'
            raise exceptions.AuthenticationFailed(resp)

        return user, token
