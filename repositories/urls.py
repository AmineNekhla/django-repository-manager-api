from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RepositoryViewSet, CodeFileViewSet


router = DefaultRouter()
router.register("repositories",RepositoryViewSet)
router.register("files", CodeFileViewSet)

urlpatterns = [
    path("",include(router.urls))
]