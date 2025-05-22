from rest_framework import status 
from rest_framework.response import Response
from rest_framework.views import APIView    
from app.models import *
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from .scope_decorator import user_permission
from .constants import *
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

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
    

class GetMetaData(APIView):
    def get(self , request):
        url = request.GET.get('url')
        if not url:
            return Response({'error': 'URL is required'}, status=400)

        try:
            response = requests.get(unquote(url), headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            title = (soup.find('meta', property='og:title') or {}).get('content') or soup.title.string if soup.title else None
            description = (soup.find('meta', property='og:description') or {}).get('content') or \
                        (soup.find('meta', attrs={'name': 'description'}) or {}).get('content') or None
            image = (soup.find('meta', property='og:image') or {}).get('content') or None

            return Response({
                'title': title,
                'description': description,
                'image': image,
            })
        except Exception as e:
            print(f"Error fetching metadata: {e}")
            return Response({'title': None, 'description': None, 'image': None}, status=500)
        