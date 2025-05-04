from rest_framework import status 
from rest_framework.response import Response
from rest_framework.views import APIView    
from app.models import *
from .serializers import *
from rest_framework.pagination import PageNumberPagination

class Pagination(PageNumberPagination):
    page_size = 10




class GetCommunities(APIView):
    def get(self, request):
        communities = Community.objects.filter(tenant= request.tenant).order_by('-created_at')
        serializer = CommunitySerializer(communities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)