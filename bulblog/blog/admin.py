from django.contrib import admin

from . import models


class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(models.Blog, BlogAdmin)
admin.site.register(models.Categories, CategoriesAdmin)
