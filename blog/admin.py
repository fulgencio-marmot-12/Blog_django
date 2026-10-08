from django.contrib import admin
from django.db.models import Count

from .models import Comment, Post


class CommentInline(admin.TabularInline):

    model = Comment
    extra = 0
    can_delete = True
    verbose_name = "comentario"
    verbose_name_plural = "comentarios"
    fields = ("name", "email", "body", "created_at")
    readonly_fields = ("name", "email", "body", "created_at")

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "published", "published_at", "cantidad_comentarios")
    list_filter = ("published", "published_at")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    ordering = ("-published_at",)
    readonly_fields = ("created_at",)
    inlines = [CommentInline]
    fieldsets = (
        (None, {"fields": ("title", "slug", "excerpt", "content")}),
        ("Multimedia", {"fields": ("image",)}),
        (
            "Publicación",
            {"fields": ("published", "published_at", "created_at")},
        ),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(total_comentarios=Count("comments"))

    @admin.display(description="Comentarios", ordering="total_comentarios")
    def cantidad_comentarios(self, obj):
        return obj.total_comentarios


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "name", "email", "created_at")
    list_filter = ("created_at", "post")
    search_fields = ("name", "email", "body")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    list_select_related = ("post",)
    readonly_fields = ("created_at",)
    fields = ("post", "name", "email", "body", "created_at")
    list_per_page = 20
