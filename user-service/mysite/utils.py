from rest_framework_simplejwt.tokens import RefreshToken
from app.models import TenantUsers

def create_user_scope(user,request):
    """
     hasStaffPermission = models.BooleanField(default=False)
    hasBlogPermission = models.BooleanField(default=False)
    hasCommunityPermission = models.BooleanField(default=False)
    hasNewsletterPermission = models.BooleanField(default=False)
    hasCoursesPermission = models.BooleanField(default=False)
    hasBuilderPermission = models.BooleanField(default=False)
    
    """
    tenant = request.tenant

    tenantuser = TenantUsers.objects.get(user=user, tenant=tenant)
    refresh = RefreshToken.for_user(user)

    scope_data = {
        'is_superuser': user.is_superuser,
        'platform_staff' : user.is_staff,
        'is_staff': tenantuser.is_staff,
        'is_admin': tenantuser.is_admin,
        'banned': tenantuser.banned,
        'blocked': tenantuser.blocked,
        'hasStaffPermission': tenantuser.hasStaffPermission,
        'hasBlogPermission': tenantuser.hasBlogPermission,
        'hasCommunityPermission': tenantuser.hasCommunityPermission,
        'hasNewsletterPermission': tenantuser.hasNewsletterPermission,
        'hasCoursesPermission': tenantuser.hasCoursesPermission,
        'hasBuilderPermission': tenantuser.hasBuilderPermission
        
    }

    refresh['scope'] = scope_data
    refresh['tenant'] = tenant.subdomain

    # Also attach to access token
    access = refresh.access_token
    access['scope'] = scope_data
    access['tenant'] = tenant.subdomain

    return {
        'refresh': refresh,
        'access': access,
    }