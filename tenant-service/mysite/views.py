from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from app.models import *
from app.serializers import *




class TenantView(APIView):
    def get(self, request):
        print(request.tenant)
        try:
            tenant = Tenants.objects.get(id=request.tenant.id)
            serializer = TenantSerializer(tenant)

            data= serializer.data
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error': 'Invalid tenant'}, status=status.HTTP_400_BAD_REQUEST)



    def post(self, request ):
        user = request.user
        tenant = Tenants.objects.filter(admin=user)
        if tenant.exists():
            return Response({'error': 'You already have a tenant'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TenantSerializer(data=request.data, context={'request': request})
        print(request.data)
        if serializer.is_valid():
            frontend = f"{request.data.get('subdomain')}.theadome.xyz"
            print(frontend)
            tenant_instance = serializer.save(admin=request.user)
            Domain.objects.create(tenant=tenant_instance , domain=frontend)
            # return Response( status=status.HTTP_201_CREATED)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self,request,subdomain):
        import time
        tenant = Tenants.objects.get(subdomain=subdomain)
        # time.sleep(5)
        serializer = TenantSerializer(tenant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MetadataView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        tenant = request.tenant
        serializer = TenantSerializer(tenant)
        return Response(serializer.data , status=status.HTTP_200_OK)






class GetTenantSchema(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        data = request.data
        print(data)
        domain = data.get('domain')
        domain = Domain.objects.filter(domain=domain)
        if domain.exists():
            domain = domain.first()
            return Response({'schemaName' : domain.tenant.subdomain},status=200)
        return Response(status=400)

