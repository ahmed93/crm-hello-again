from rest_framework.routers import DefaultRouter

from .views import AddressViewSet, AppUserJoinedViewSet, CustomerRelationshipViewSet

router = DefaultRouter()
router.register(r"users", AppUserJoinedViewSet, basename="users")
router.register(r"addresses", AddressViewSet, basename="addresses")
router.register(r"relationships", CustomerRelationshipViewSet, basename="relationships")

urlpatterns = router.urls
