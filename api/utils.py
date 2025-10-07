# utils.py
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from .models import UserMaster
from rest_framework.response import Response
from rest_framework import status

def create_jwt(payload):
    payload = payload.copy()
    payload['exp'] = datetime.utcnow() + timedelta(days=730)
    payload['iat'] = datetime.utcnow()
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

def decode_jwt(token):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        print("⚠️ Token expired")
        return None
    except jwt.InvalidTokenError as e:
        print("⚠️ Invalid token:", e)
        return None

def create_user_tokens(user):
    payload = {
        'reg_id': str(user.reg_id),
        'number': str(user.mobile),
        'type': 'access'
    }
    return create_jwt(payload)

def verify_user_token(token):
    payload = decode_jwt(token)
    print("Decoded payload:", payload)
    if not payload:
        return None
    if payload.get('type') != 'access' or 'reg_id' not in payload:
        return None
    try:
        user = UserMaster.objects.get(reg_id=payload['reg_id'])
        return user
    except UserMaster.DoesNotExist:
        return None

def get_user_from_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None, Response({
            "data": "Token not available",
            "status": "failed",
            "statusCode": status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)
    
    token = auth_header.split(' ')[1]
    user = verify_user_token(token)
    if not user:
        return None, Response({
            "data": "Token expired or user not available",
            "status": "failed",
            "statusCode": status.HTTP_401_UNAUTHORIZED       
        }, status=status.HTTP_401_UNAUTHORIZED)
    return user, None
