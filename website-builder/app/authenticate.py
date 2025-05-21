from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth.models import AnonymousUser
from . models import  UserCache,TenantUsers
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
        
        tenant = request.tenant
        access = AccessToken(raw_token)
        if access['tenant'] != tenant.subdomain :
            return None
        # print(f"tenant is {tenant}")
        request.scope = access['scope']


        
        tenantuser = TenantUsers.objects.filter(user=user, tenant=tenant)
        # print(tenantuser)

        if  tenantuser.exists() :
            request.tenantuser = tenantuser.first()
        elif user.is_superuser:
            pass
        else:
            raise AuthenticationFailed("Tenant user not found.")
        
     
        user.is_authenticated = True
        return user, validated_token 
    


    