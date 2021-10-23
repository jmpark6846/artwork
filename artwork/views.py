from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from artwork.models import Artwork, ProductPreset, Product
from artwork.serializers import ArtworkSerializer, ProductPresetSerializer, ProductSerializer


class ArtworkViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ArtworkSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Artwork.objects.filter(user=self.request.user)

    @action(detail=True, methods=['GET'])
    def presets(self, request, **kwargs):
        artwork = self.get_object()
        preset_set = set()
        for product in artwork.product_set.all():
            preset_set.add(product.preset)

        context = self.get_serializer_context()
        context.update({'artwork': artwork})
        data = ProductPresetSerializer(list(preset_set), many=True, context=context).data
        return Response(data, status=200)


class ProductPresetViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductPresetSerializer

    def get_queryset(self):
        return ProductPreset.objects.order_by('name')

    def get_serializer_context(self):
        context = super(ProductPresetViewSet, self).get_serializer_context()
        artwork_id = self.request.query_params.get('artwork_id')
        if artwork_id is not None:
            artwork = Artwork.objects.get(id=artwork_id)
            context.update({"artwork": artwork})
        return context


class ProductViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = Product.objects.filter(user=self.request.user)
        artwork_id = self.request.query_params.get('artwork_id')
        preset_id = self.request.query_params.get('preset_id')

        if artwork_id is not None:
            qs = qs.filter(artwork_id=artwork_id)

        if preset_id is not None:
            qs = qs.filter(preset_id=preset_id)
        return qs.order_by('name')

    def get_serializer_context(self):
        context = super(ProductViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        return context

    @action(detail=False, methods=['POST'], url_path='toggle')
    def toggle_or_create_product(self, request, *args, **kwargs):
        result_list = []
        response = Response()

        for preset_data in request.data:
            preset = ProductPreset.objects.get(id=preset_data['preset'])
            product = preset.product_set.filter(artwork_id=preset_data['artwork']).last()

            if product:
                product.is_active = preset_data['is_active']
                product.save()
                response.status_code = status.HTTP_201_CREATED
            else:
                serializer = ProductSerializer(data=preset_data)
                response.status_code = status.HTTP_200_OK
                serializer.is_valid(raise_exception=True)
                product = serializer.save()

            result_list.append(product)

        response.data = ProductSerializer(result_list, many=True).data
        return response
