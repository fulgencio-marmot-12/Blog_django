from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CommentForm, PostForm
from .models import Post


class SoloAdmin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Solo el administrador puede hacer esto.")
        return super().handle_no_permission()


class PostListView(ListView):

    model = Post
    template_name = "blog/post_list.html"
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(published=True)


class PostDetailView(DetailView):

    model = Post
    template_name = "blog/post_detail.html"

    def get_queryset(self):
        return Post.objects.filter(published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comentarios"] = self.object.comments.all()
        context.setdefault("form", CommentForm())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = self.object
            comentario.save()
            messages.success(request, "Gracias por tu comentario, ya está publicado.")
            return redirect("blog:detalle", slug=self.object.slug)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)


class PostCreateView(SoloAdmin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        messages.success(self.request, "La entrada se creó correctamente.")
        return super().form_valid(form)


class PostUpdateView(SoloAdmin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Guardaste los cambios de la entrada.")
        return super().form_valid(form)


class PostDeleteView(SoloAdmin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:lista")

    def form_valid(self, form):
        messages.success(self.request, "La entrada se borró.")
        return super().form_valid(form)
