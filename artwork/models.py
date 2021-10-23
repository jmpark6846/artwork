from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save


def artwork_directory_path(instance, filename):
    return 'artwork/{0}/{1}'.format(instance.user.username, filename)


class Artwork(models.Model):
    title = models.CharField(max_length=120, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='artworks')
    tags = models.ManyToManyField('artwork.Tag', blank=True)
    description = models.TextField(blank=True, null=True)
    file = models.ImageField(upload_to=artwork_directory_path, blank=True, null=True)

    def __str__(self):
        return '{}_{}'.format(self.id, self.title)


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


def product_preset_directory_path(instance, filename):
    return 'product_preset/{0}/{1}'.format(instance.id, filename)


class ProductPreset(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to=product_preset_directory_path, blank=True, null=True)

    def __str__(self):
        return '{}_{}'.format(self.id, self.name)


def product_image_directory_path(instance, filename):
    return 'product_image/{0}/{1}'.format(instance.id, filename)


class Product(models.Model):
    name = models.CharField(max_length=120)
    price = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    preset = models.ForeignKey(ProductPreset, on_delete=models.NOT_PROVIDED)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_directory_path, blank=True, null=True)

    def __str__(self):
        return '{}_{}'.format(self.id, self.name)
