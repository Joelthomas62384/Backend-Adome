from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.models import *
from .serializers import *
from .scope_decorator import user_permission
from django.core.cache import cache
from . utils import tenant_key_prefix , website_list_cache_key , website_cache_key , default_website_cache_key

from . import constants

class WebsiteApiView(APIView):

    @user_permission(constants.HAS_BUILDER_PERMISSION)
    def get(self, request):
        cache_key = website_list_cache_key(request.tenant)
        data = cache.get(cache_key)
        if data is not None:
            print("From Cache")
            return Response(data)
        queryset = Website.objects.filter(tenant=request.tenant).order_by("-is_default", "-updated_at")
        serializer = WebsiteSerialzer(queryset, many=True, context={'request': request})
        cache.set(cache_key, serializer.data, timeout=None)
        return Response(serializer.data)

    @user_permission(constants.HAS_BUILDER_PERMISSION)    
    def post(self, request):
        
        serializer = WebsiteSerialzer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(tenant=request.tenant,is_default=(not Website.objects.filter(tenant=request.tenant, is_default=True).exists()))
            cache.delete(website_list_cache_key(request.tenant))
            cache.delete(default_website_cache_key(request.tenant))
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
            cache.delete(website_list_cache_key(request.tenant))
            if website.is_default:
                cache.delete(default_website_cache_key(request.tenant))
            if 'id' in locals():  # for put and delete
                cache.delete(website_cache_key(request.tenant, id))
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @user_permission(constants.HAS_BUILDER_PERMISSION)   
    def delete(self, request, id):
        website = Website.objects.filter(tenant=request.tenant, id=id).first()
        if not website:
            return Response({'data': 'Website not found'}, status=status.HTTP_404_NOT_FOUND)
        website.delete()
        cache.delete(website_list_cache_key(request.tenant))
        if website.is_default:
            cache.delete(default_website_cache_key(request.tenant))
        if 'id' in locals():  # for put and delete
            cache.delete(website_cache_key(request.tenant, id))
        return Response({'data': 'Website deleted successfully'}, status=status.HTTP_200_OK)




class GetWebsiteView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, id):
        cache_key = website_cache_key(request.tenant, id)
        data = cache.get(cache_key)
        if data:
            print("From Cache")
            return Response(data)
        website = Website.objects.filter(tenant=request.tenant, id=id).first()
        if not website:
            return Response({'data': 'Website not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = WebsiteSerialzer(website, context={'request': request})
        cache.set(cache_key, serializer.data, timeout=None)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GetTenantDefaultWebpage(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        cache_key = default_website_cache_key(request.tenant)
        data = cache.get(cache_key)
        if data:
            print("From Cache")
            return Response(data)

        website = Website.objects.filter(tenant=request.tenant, is_default=True).first()
        if not website:
            return Response({'data': "Website not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = WebsiteSerialzer(website, context={'request': request})
        cache.set(cache_key, serializer.data, timeout=60 * 10)
        return Response(serializer.data, status=status.HTTP_200_OK)



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
            cache.delete(website_list_cache_key(request.tenant))
            cache.delete(default_website_cache_key(request.tenant))
            cache.delete(website_cache_key(request.tenant, id))

        serializer = WebsiteSerialzer(website, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
