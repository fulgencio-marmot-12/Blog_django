from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title", "excerpt", "content", "image", "published", "published_at")
        labels = {
            "title": "Título",
            "excerpt": "Extracto",
            "content": "Contenido",
            "image": "Imagen",
            "published": "Publicado",
            "published_at": "Fecha de publicación",
        }
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Título de la entrada"}),
            "excerpt": forms.Textarea(
                attrs={
                    "rows": 2,
                    "placeholder": "Resumen corto que se ve en la lista del blog",
                }
            ),
            "content": forms.Textarea(
                attrs={"rows": 14, "placeholder": "Escribí la entrada acá..."}
            ),
            "published_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ("name", "email", "body")
        labels = {
            "name": "Nombre",
            "email": "Email",
            "body": "Comentario",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Tu nombre", "autocomplete": "name"}
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Tu email (no se publica)",
                    "autocomplete": "email",
                }
            ),
            "body": forms.Textarea(
                attrs={"placeholder": "Escribí tu comentario...", "rows": 4}
            ),
        }
