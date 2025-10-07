# api/authentication.py
from rest_framework import authentication, exceptions
from django.contrib.auth import get_user_model

from bookmygame.api.utils import decode_jwt
# from api.utils import decode_jwt

User = get_user_model()

class CustomJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None  # no authentication provided

        try:
            prefix, token = auth_header.split()
        except ValueError:
            raise exceptions.AuthenticationFailed('Invalid Authorization header format.')

        if prefix.lower() != 'bearer':
            raise exceptions.AuthenticationFailed('Authorization header must start with Bearer.')

        payload = decode_jwt(token)
        if not payload:
            raise exceptions.AuthenticationFailed('Invalid or expired token.')

        user_id = payload.get('reg_id')  # match your payload key
        if not user_id:
            raise exceptions.AuthenticationFailed('Token missing reg_id.')

        try:
            user = User.objects.get(reg_id=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('User not found.')

        return (user, token)
