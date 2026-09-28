from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Cart, CartItem, Order, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount_price', 'in_stock', 'is_new', 'is_bestseller', 'image_preview')
    list_filter = ('category', 'in_stock', 'is_new', 'is_bestseller')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:8px;" />', obj.image.url)
        return '—'
    image_preview.short_description = 'Фото'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status',)
    list_editable = ('status',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'is_verified', 'created_at')
    list_filter = ('rating', 'is_verified')


admin.site.register(Cart)
admin.site.register(CartItem)
