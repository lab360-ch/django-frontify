from django.contrib import admin

from example.models import ExampleImageModel


@admin.register(ExampleImageModel)
class ExampleImageModelAdmin(admin.ModelAdmin):
    pass

