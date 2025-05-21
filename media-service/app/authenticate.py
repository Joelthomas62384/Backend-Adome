from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.models import AnonymousUser
from . models import  UserCache
from rest_framework_simplejwt.tokens import AccessToken

class CustomJwtAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = UserCache
    def authenticate(self, request):
        subdomain = request.tenant.subdomain
        raw_token = request.COOKIES.get(f'{subdomain}_access_token')
        refresh_token = request.COOKIES.get(f'{subdomain}_refresh_token')
        if not raw_token or not refresh_token:
            return None  

        try:
            validated_token = self.get_validated_token(raw_token)
        except (InvalidToken, TokenError) as e:
            raise AuthenticationFailed("Invalid or expired access token.") from e

        user = self.get_user(validated_token)

        if user is None:
            raise AuthenticationFailed("User not found.")
        access = AccessToken(raw_token)
        if access['tenant'] != request.tenant.subdomain :
            return None
        
        
     
        user.is_authenticated = True
        # user.is_active = True
        return user, validated_token 
    


    