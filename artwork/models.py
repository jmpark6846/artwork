from django.conf import settings
from django.db import models


def artwork_directory_path(instance, filename):
    return 'artwork/{0}/{1}'.format(instance.user.username, filename)


class Artwork(models.Model):
    title = models.CharField(max_length=120)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='artworks')
    tags = models.ManyToManyField('issue.Tag')
    description = models.TextField()
    file = models.FileField(upload_to=artwork_directory_path, blank=True, null=True)


class Tag(models.Model):
    name = models.CharField(max_length=30)


def product_preset_directory_path(instance, filename):
    return 'product_preset/{0}/{1}'.format(instance.name, filename)


class ProductPreset(models.Model):
    name = models.CharField(max_length=120)
    is_active = models.BooleanField(default=False)
    image = models.ImageField(upload_to=product_preset_directory_path, blank=True, null=True)


class Product(ProductPreset):
    price = models.PositiveIntegerField()

