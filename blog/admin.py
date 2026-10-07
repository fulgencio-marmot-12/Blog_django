from django.contrib import admin

from .models import Comment, Post


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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "name", "email", "created_at")
    list_filter = ("created_at", "post")
    search_fields = ("name", "email", "body")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    list_select_related = ("post",)
