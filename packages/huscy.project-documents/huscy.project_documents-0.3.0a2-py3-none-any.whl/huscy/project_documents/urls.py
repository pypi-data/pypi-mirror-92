from rest_framework.routers import DefaultRouter

from huscy.project_documents import views


router = DefaultRouter()
router.register('documents', views.DocumentViewSet)
router.register('documenttypes', views.DocumentTypeViewSet)
router.register('projects', views.ProjectViewSet)
