from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "published", "published_at", "created_at")
    list_filter = ("published", "published_at")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    ordering = ("-published_at",)
    fieldsets = (
        (None, {"fields": ("title", "slug", "excerpt", "content")}),
        ("Multimedia", {"fields": ("image",)}),
        ("Publicacion", {"fields": ("published", "published_at")}),
    )
