from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.models import AnonymousUser
from . models import  UserCache , TenantUsers

class CustomJwtAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = UserCache
    def authenticate(self, request):
        raw_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if not raw_token or not refresh_token:
            return None  

        try:
            validated_token = self.get_validated_token(raw_token)
        except (InvalidToken, TokenError) as e:
            raise AuthenticationFailed("Invalid or expired access token.") from e

        user = self.get_user(validated_token)

        print(user)

        if user is None:
            raise AuthenticationFailed("User not found.")
        
        tenant = request.tenant
        
     
        user.is_authenticated = True

        tenantuser = TenantUsers.objects.filter(user=user, tenant=tenant)
        if not tenantuser.exists():
            return None
        request.tenantuser = tenantuser.first()

        return user, validated_token 
    


    
