from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from app.models import Comment
from .serializers import CommentSerializer

class CommentPagination(PageNumberPagination):
    page_size = 10

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get_queryset(self):
        parent = self.request.query_params.get('parent')
        contentType = self.request.query_params.get('contentType')
        contentId = self.request.query_params.get('contentId')
        qs = Comment.objects.all()
        if parent == 'null':
            qs = qs.filter(contentType=contentType, contentId=contentId, parent__isnull=True)
        elif parent:
            qs = qs.filter(parent_id=parent)
        return qs.order_by('-created_at')