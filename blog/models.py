from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class Post(models.Model):
    """Una entrada del blog: texto, imagen y fecha de publicacion."""

    title = models.CharField("titulo", max_length=200)
    slug = models.SlugField("enlace", max_length=220, unique=True, blank=True)
    excerpt = models.CharField(
        "extracto",
        max_length=300,
        help_text="Resumen corto que se muestra en la lista del blog.",
    )
    content = models.TextField("contenido")
    image = models.ImageField(
        "imagen",
        upload_to="posts/",
        blank=True,
        help_text="Imagen de la entrada (opcional). Se guarda en media/posts/.",
    )
    published = models.BooleanField("publicado", default=True)
    created_at = models.DateTimeField("creado el", auto_now_add=True)
    published_at = models.DateTimeField("publicado el", default=timezone.now)

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "entrada"
        verbose_name_plural = "entradas"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:180] or "entrada"
            slug = base
            contador = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                contador += 1
                slug = f"{base}-{contador}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:detalle", args=[self.slug])
