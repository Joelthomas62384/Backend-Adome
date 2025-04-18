from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import *
from .serializers import *
from .scope_decorator import user_permission

from . import constants

class WebsiteApiView(APIView):

    @user_permission(constants.HAS_BUILDER_PERMISSION)
    def get(self, request):
        queryset = Website.objects.filter(tenant=request.tenant).order_by("-is_default", "-updated_at")
        serializer = WebsiteSerialzer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @user_permission(constants.HAS_BUILDER_PERMISSION)    
    def post(self, request):
        
        serializer = WebsiteSerialzer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(tenant=request.tenant,is_default=(not Website.objects.filter(tenant=request.tenant, is_default=True).exists()))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @user_permission(constants.HAS_BUILDER_PERMISSION)   
    def put(self ,request , id):
        website = Website.objects.filter(tenant=request.tenant, id=id).first()
        if not website:
            return Response({'data': 'Website not found'}, status=status.HTTP_404_NOT_FOUND)    
        serializer = WebsiteSerialzer(website, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @user_permission(constants.HAS_BUILDER_PERMISSION)   
    def delete(self, request, id):
        website = Website.objects.filter(tenant=request.tenant, id=id).first()
        if not website:
            return Response({'data': 'Website not found'}, status=status.HTTP_404_NOT_FOUND)
        website.delete()
        return Response({'data': 'Website deleted successfully'}, status=status.HTTP_200_OK)




class GetWebsiteView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, id):
        website = Website.objects.filter(tenant=request.tenant, id=id).first()
        if not website:
            return Response({'data': 'Website not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WebsiteSerialzer(website, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class GetTenantDefaultWebpage(APIView):
    authentication_classes = []
    permission_classes = []


    def get(self, request):
        website = Website.objects.filter(tenant=request.tenant , is_default=True)
        # print(website.first().web_data)
        if not website.exists():
            return Response({'data' : "Website not found"} , status=status.HTTP_404_NOT_FOUND)
        serializer = WebsiteSerialzer(website.first() , context = {'request' , request})
        return Response(serializer.data , status=status.HTTP_200_OK)



class ChangeTenantDefaultWebpage(APIView):
    """
    Set one website as the default for a tenant, remove default from all others.
    """
    @user_permission(constants.HAS_BUILDER_PERMISSION)   
    def put(self, request, id):
        website = Website.objects.filter(tenant=request.tenant, id=id).first()
        if not website:
            return Response({'data': 'Website not found'}, status=status.HTTP_404_NOT_FOUND)

        Website.objects.filter(tenant=request.tenant, is_default=True).exclude(id=website.id).update(is_default=False)

        if not website.is_default:
            website.is_default = True
            website.save()

        serializer = WebsiteSerialzer(website, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
