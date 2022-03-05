from django.contrib import admin
from webapp.models import Product, Review


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'description']
    fields = ['title', 'category', 'description', 'picture']


admin.site.register(Product, ProductAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'author', 'rate']
    fields = ['id', 'product', 'author', 'review_text', 'rate', 'is_moderated']


admin.site.register(Review, ReviewAdmin)