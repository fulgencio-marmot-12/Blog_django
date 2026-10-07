from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """Formulario para dejar un comentario sin registrarse."""

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
                attrs={"placeholder": "Escribi tu comentario...", "rows": 4}
            ),
        }
