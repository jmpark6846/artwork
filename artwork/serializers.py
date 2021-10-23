from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from artwork.models import Artwork, ProductPreset, Product


class ArtworkSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Artwork
        fields = '__all__'

    def get_products(self, obj: Artwork):
        return ProductSerializer(obj.product_set, many=True, context=self.context).data


class ProductPresetSerializer(serializers.ModelSerializer):
    enabled = serializers.SerializerMethodField()

    class Meta:
        model = ProductPreset
        fields = '__all__'

    def get_enabled(self, obj: ProductPreset):
        artwork = self.context.get('artwork')
        return obj.product_set.filter(artwork=artwork, is_active=True).exists()


class ProductArtworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artwork
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Product
        fields = '__all__'

    def to_internal_value(self, data):
        import base64
        import sys
        from io import BytesIO

        data['image'] = data['image'].replace('data:image/png;base64,', '')
        img_bytes = BytesIO(base64.b64decode(data['image']))
        img = InMemoryUploadedFile(
            img_bytes,
            'file',
            name=data['name'] + '.png',
            content_type="image/png",
            size=sys.getsizeof(img_bytes),
            charset=None)

        data['image'] = img

        return super(ProductSerializer, self).to_internal_value(data)

    def to_representation(self, instance: Product):
        result = super(ProductSerializer, self).to_representation(instance)
        if not instance.image:
            result['image'] = ProductPresetSerializer(instance.preset, context=self.context).data['image']

        artwork = Artwork.objects.get(id=result['artwork'])
        result['artwork'] = ProductArtworkSerializer(artwork, context=self.context).data
        return result

    def create(self, validated_data):
        validated_data['name'] = '{} {}'.format(validated_data['artwork'].title, validated_data['preset'].name)
        return super(ProductSerializer, self).create(validated_data)
