from django.contrib import admin
from .models import VendorProfile, Product, Review


@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'location', 'phone', 'website']
    list_filter = ['category']
    search_fields = ['name', 'location', 'category']
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'category', 'location', 'photo')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'website')
        }),
        ('About', {
            'fields': ('story',)
        }),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor', 'price']
    list_filter = ['vendor']
    search_fields = ['name', 'vendor__name']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor', 'rating']
    list_filter = ['rating', 'vendor']
    search_fields = ['name', 'vendor__name', 'comment']
