from rest_framework.reverse import reverse
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED


def test_list_documents_is_not_provided(client):
    response = list_documents(client)

    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED


def test_retrieve_documents_is_not_provided(client, document):
    response = retrieve_document(client, document)

    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED


def list_documents(client):
    return client.get(reverse('document-list'))


def retrieve_document(client, document):
    return client.get(reverse('document-detail', kwargs=dict(pk=document.pk)))
