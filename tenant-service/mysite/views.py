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
        if serializer.is_valid():
            serializer.save(admin=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def put(self,request,id):
        tenant = Tenants.objects.get(id=id)
        serializer = TenantSerializer(tenant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





