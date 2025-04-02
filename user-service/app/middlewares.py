from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from .models import Tenants

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path.strip('/').split('/')
        print(path)
        
        if len(path) < 2:
            return JsonResponse({'error': 'Invalid request path'}, status=400)
        
        service, tenant_subdomain, *newpath = path

        tenant = Tenants.objects.filter(subdomain=tenant_subdomain).first()
        # print(tenant)
        if not tenant:
            return JsonResponse({'error': 'Invalid tenant'}, status=404)

        request.tenant = tenant
        request.path_info = "/" + "/".join(newpath) 
        print(request.path_info)


