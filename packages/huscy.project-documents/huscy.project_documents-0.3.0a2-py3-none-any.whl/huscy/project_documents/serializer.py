from rest_framework import serializers

from huscy.project_documents import models, services


class DocumentSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    document_type_name = serializers.SerializerMethodField()

    class Meta:
        model = models.Document
        fields = (
            'creator',
            'document_type',
            'document_type_name',
            'filehandle',
            'filename',
            'project',
            'uploaded_at',
            'uploaded_by',
        )
        read_only_fields = 'creator', 'filename', 'uploaded_at', 'uploaded_by'

    def get_document_type_name(self, document):
        return document.document_type.name

    def create(self, validated_data):
        return services.create_document(**validated_data)


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DocumentType
        fields = (
            'id',
            'name',
        )


class ProjectSerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField()

    class Meta:
        model = models.Project
        fields = (
            'id',
            'documents',
        )

    def get_documents(self, project):
        documents = services.get_documents(project)
        return DocumentSerializer(documents, many=True).data
