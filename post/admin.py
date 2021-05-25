from django.contrib import admin
from .models import MainTitle, SubTitle, Category

# Register your models here.

@admin.register(MainTitle)
class MainTitleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display=['title','created_on']


@admin.register(SubTitle)
class SubTitleAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('title',)}
    list_display=['title','created_on','available_on']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pulated_fields={'slug':('name',)}
    list_display=['name','slug','created_on']
