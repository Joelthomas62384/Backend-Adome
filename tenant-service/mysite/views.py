from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from app.models import *
from app.serializers import *




class TenantView(APIView):

    def post(self, request, ):
        serializer = TenantSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(admin=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





