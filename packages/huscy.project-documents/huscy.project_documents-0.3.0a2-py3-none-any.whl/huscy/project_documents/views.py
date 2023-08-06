from rest_framework import mixins, viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from huscy.project_documents import models, serializer, services


class DocumentViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = services.get_documents()
    serializer_class = serializer.DocumentSerializer


class DocumentTypeViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = (DjangoModelPermissions, )
    queryset = services.get_document_types()
    serializer_class = serializer.DocumentTypeSerializer


class ProjectViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = models.Project.objects.all()
    serializer_class = serializer.ProjectSerializer
