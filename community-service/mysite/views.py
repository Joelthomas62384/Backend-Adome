from rest_framework import status 
from rest_framework.response import Response
from rest_framework.views import APIView    
from app.models import *
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from .scope_decorator import user_permission
from .constants import *

class Pagination(PageNumberPagination):
    page_size = 20





class GetCommunities(APIView):
    @user_permission(HAS_COMMUNITY_PERMISSION)
    def get(self, request):
        communities = Community.objects.filter(tenant= request.tenant).order_by('-created_at')
        serializer = CommunitySerializer(communities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class GetCommunitiesUser(APIView):
    def get(self, request):
        communities = Community.objects.filter(tenant=request.tenant,communitymembers__user=request.tenantuser).order_by('-created_at')
        serializer = CommunitySerializer(communities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class GetMessages(APIView):
    def get(self , request ,id):
        paginator = Pagination()
        messages = CommunityChats.objects.filter(community__id = id).order_by("-created_at")
        paginated_messages = paginator.paginate_queryset(messages, request, view=self)
        serializer = CommunityChatSerializer(paginated_messages , many=True)
        
        return paginator.get_paginated_response(serializer.data)