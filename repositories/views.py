from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Repository, CodeFile
from .serializers import RepositorySerializer, CodeFileSerializer
from .filters import CodeFileFilter
from .services import CodeFileService


class RepositoryViewSet(viewsets.ModelViewSet):
    queryset = Repository.objects.all().order_by("-created_at")
    serializer_class = RepositorySerializer


class CodeFileViewSet(viewsets.ModelViewSet):
    queryset = CodeFile.objects.all().order_by("-added_at")
    serializer_class = CodeFileSerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CodeFileFilter
    search_fields = ["name", "language", "file_type", "description"]
    ordering_fields = ["size", "added_at", "name"]

    def perform_create(self, serializer):
        """
        We intercept the DRF save process to delegate business logic to our Service Layer.
        """
        CodeFileService.create_code_file(serializer.validated_data)

    @action(detail=False, methods=["get"])
    def critical(self, request):
        """
        Restored endpoint specifically requested by the Verification Plan.
        It uses our highly optimized custom Manager/QuerySet underneath!
        """
        critical_files = CodeFile.objects.critical()
        # We manually paginate here if needed, or just return the data directly
        page = self.paginate_queryset(critical_files)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(critical_files, many=True)
        return Response(serializer.data)