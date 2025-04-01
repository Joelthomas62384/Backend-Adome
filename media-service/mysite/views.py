
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView



class PostImageView(APIView):
    def post(self, request):
        serializer = LogoImagesSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class PostTenantImageView(APIView):
    def post(self, request):
        serializer = TenantImageBucketSerializer(data = request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user, tenant=request.tenant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
