from typing import Optional

from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Note
from .serializers import NoteSerializer


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination class.
    """
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# PUBLIC_INTERFACE
@api_view(['GET'])
def health(request):
    """Health check endpoint to verify the server is running."""
    return Response({"message": "Server is up!"})


# PUBLIC_INTERFACE
class NoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows notes to be viewed or edited.

    Supported operations:
    - list: GET /api/notes/?search=<text> or ?title=<text>
    - create: POST /api/notes/
    - retrieve: GET /api/notes/{id}/
    - update: PUT /api/notes/{id}/
    - partial_update: PATCH /api/notes/{id}/
    - destroy: DELETE /api/notes/{id}/
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]  # enables ?search= query param

    def get_queryset(self):
        """
        Optionally filter by exact/contains title via ?title= convenience query param.
        Falls back to DRF's SearchFilter when ?search= is used.
        """
        qs = super().get_queryset()
        title: Optional[str] = self.request.query_params.get("title")
        if title:
            qs = qs.filter(title__icontains=title)
        return qs

    @action(detail=False, methods=['get'], url_path='count')
    def count(self, request):
        """Return count of notes, useful for quick stats."""
        return Response({"count": self.get_queryset().count()}, status=status.HTTP_200_OK)
