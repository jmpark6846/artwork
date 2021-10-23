from django.contrib import admin

# Register your models here.
from artwork.models import ProductPreset, Product, Artwork

admin.site.register(Artwork)
admin.site.register(Product)
admin.site.register(ProductPreset)
