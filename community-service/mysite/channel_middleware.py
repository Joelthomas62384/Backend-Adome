from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.db import close_old_connections
from app.models import Tenants, TenantUsers, UserCache
from asgiref.sync import sync_to_async

class AuthenticationMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        close_old_connections()
        scope['user'] = AnonymousUser()
        scope['tenant'] = None
        scope['tenantuser'] = None
        scope['userscope'] = None
        path = scope.get("path", "")
        parts = path.strip("/").split("/")
        if len(parts) >= 4 and parts[0] == "community":
            tenant_path = parts[1]
            
            cookies = scope.get("cookies", {})
            access_token = cookies.get(f"{tenant_path}_access_token")

            if access_token:
                try:
                    token = AccessToken(access_token)
                    tenant = token['tenant']
                    user_id = token['user_id']
                    userscope = token['scope']

                    tenant_obj = await self.get_tenant(tenant)
                    
                    user = await self.get_user(user_id)
                    
                    if user is None or not user.is_active:  
                        scope['user'] = AnonymousUser()
                        return await self.app(scope, receive, send)

                    tenantuser = await self.get_tenantuser(user, tenant_obj)

                    scope['tenant'] = tenant_obj
                    scope['user'] = user
                    scope['tenantuser'] = tenantuser
                    scope['userscope'] = userscope

                except (InvalidToken, TokenError, Tenants.DoesNotExist, UserCache.DoesNotExist, TenantUsers.DoesNotExist) as e:
                    scope['user'] = AnonymousUser()
                    scope['tenant'] = None
                    scope['tenantuser'] = None

        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_tenant(self, tenant: str) -> Tenants:
        return Tenants.objects.get(subdomain=tenant)

    @database_sync_to_async
    def get_user(self, user_id: int) -> UserCache:
        try:
            return UserCache.objects.get(id=user_id)
        except UserCache.DoesNotExist:
            return None

    @database_sync_to_async
    def get_tenantuser(self, user: UserCache, tenant: Tenants) -> TenantUsers:
        return TenantUsers.objects.get(user=user, tenant=tenant)