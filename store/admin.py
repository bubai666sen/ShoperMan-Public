from django.contrib import admin
from .models.product import Products
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order
from .models.tags import Tag
from django.utils.html import format_html

class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer','product','price','phone','date','status']
    list_display_links = ('product', 'customer')

class AdminProduct(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}" width="auto" height="200px" />'.format(obj.image.url))

    image_tag.short_description = 'Image'

    list_display = ['image_tag','name', 'category','price',]
    readonly_fields = ['image_tag']
    list_display_links = ('image_tag', 'name')
    autocomplete_fields = ['tags']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']

# Register your models here.
admin.site.register(Products,AdminProduct)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order,OrderAdmin)
admin.site.register(Tag,TagAdmin)


# username = Tanushree, email = tanushree7252@gmail.com, password = 1234
