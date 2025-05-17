from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def user_permission(required_permission):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self , request, *args, **kwargs):
            print(request)
            scope = getattr(request, 'scope', {})
            print(scope)

            if not scope:
                
                return Response({'detail': 'Unauthorized: Missing scope.'}, status=status.HTTP_401_UNAUTHORIZED)

            if scope.get('is_admin') or (scope.get('is_staff') and scope.get(required_permission)):
                return view_func(self ,request, *args, **kwargs)

            return Response({'detail': 'Unauthorized: Insufficient permissions.'}, status=status.HTTP_403_FORBIDDEN)
        
        return _wrapped_view
    return decorator