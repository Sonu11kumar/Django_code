from django.contrib import admin
from .models import Album, Post, Profile, Order, OrderItem, Product


class PostModelAdmin (admin.ModelAdmin):
    list_display = ["title", "updated", "timestamp", "image"]
    list_display_links = ["updated", "timestamp"]
    list_editable = ["title"]
    list_filter = ["updated", "timestamp"]

    class Meta:
        model = Post


admin.site.register(Album)
admin.site.register(Post, PostModelAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Profile)
admin.site.register(Product)
