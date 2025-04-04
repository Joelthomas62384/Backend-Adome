from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import *
from .serializers import *




class WebsiteApiView(APIView):
    # authentication_classes = []
    # permission_classes = []
    def get(self, request):
        queryset = Website.objects.filter(tenant=request.tenant)
        serializer = WebsiteSerialzer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WebsiteSerialzer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(tenant=request.tenant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self ,request , id):
        website = Website.objects.filter(tenant=request.tenant, id=id).first()
        if not website:
            return Response({'data': 'Website not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WebsiteSerialzer(website, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id):
        website = Website.objects.filter(tenant=request.tenant, id=id).first()
        if not website:
            return Response({'data': 'Website not found'}, status=status.HTTP_404_NOT_FOUND)
        website.delete()
        return Response({'data': 'Website deleted successfully'}, status=status.HTTP_200_OK)




class GetWebsiteView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        website = Website.objects.filter(tenant=request.tenant, is_default=True).first()
        if not website:
            return Response({'data': 'Website not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WebsiteSerialzer(website, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)