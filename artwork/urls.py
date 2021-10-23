from django.urls import path, include
from rest_framework.routers import SimpleRouter

from artwork.views import ArtworkViewSet, ProductViewSet, ProductPresetViewSet

router = SimpleRouter()
router.register('artworks', ArtworkViewSet, basename='artwork')
router.register('presets', ProductPresetViewSet, basename='preset')
router.register('products', ProductViewSet, basename='product')


urlpatterns = [
    path('', include(router.urls))
]

