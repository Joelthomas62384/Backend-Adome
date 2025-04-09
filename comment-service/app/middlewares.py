from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from .models import Tenants

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path.strip('/').split('/')
        print("Raw path parts:", path)
        
        if len(path) < 2:
            return JsonResponse({'error': 'Invalid request path'}, status=400)
        
        service, tenant_subdomain, *newpath = path

        tenant = Tenants.objects.filter(subdomain=tenant_subdomain).first()
        if not tenant:
            return JsonResponse({'error': 'Invalid tenant'}, status=404)

        request.tenant = tenant
        
        # Rebuild the new path
        new_path = '/' + '/'.join(newpath)
        
        # Preserve trailing slash
        if request.path.endswith('/') and not new_path.endswith('/'):
            new_path += '/'

        request.path_info = new_path
        request.path = new_path  # optional but may help with other middleware
        print("Modified path_info:", request.path_info)
