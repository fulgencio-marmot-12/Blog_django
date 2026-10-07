from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.PostListView.as_view(), name="lista"),
    path("post/nuevo/", views.PostCreateView.as_view(), name="crear"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="detalle"),
    path("post/<slug:slug>/editar/", views.PostUpdateView.as_view(), name="editar"),
    path("post/<slug:slug>/borrar/", views.PostDeleteView.as_view(), name="borrar"),
]
