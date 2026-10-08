from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import CommentForm
from .models import Comment, Post


def crear_post(titulo, dias_atras=0, publicado=True):
    return Post.objects.create(
        title=titulo,
        excerpt=f"Extracto de {titulo}",
        content=f"Contenido de {titulo}",
        published=publicado,
        published_at=timezone.now() - timedelta(days=dias_atras),
    )


class PostModelTests(TestCase):
    def test_el_slug_se_genera_solo(self):
        post = crear_post("Primeros pasos con Django")
        self.assertEqual(post.slug, "primeros-pasos-con-django")

    def test_los_slugs_no_se_repiten(self):
        uno = crear_post("Post repetido")
        dos = crear_post("Post repetido")
        self.assertEqual(uno.slug, "post-repetido")
        self.assertEqual(dos.slug, "post-repetido-2")

    def test_str_devuelve_el_titulo(self):
        post = crear_post("Mi entrada")
        self.assertEqual(str(post), "Mi entrada")

    def test_las_entradas_se_ordenan_de_mas_nueva_a_mas_vieja(self):
        vieja = crear_post("La mas vieja", dias_atras=10)
        nueva = crear_post("La mas nueva", dias_atras=1)
        self.assertEqual(list(Post.objects.all()), [nueva, vieja])

    def test_get_absolute_url_apunta_al_detalle(self):
        post = crear_post("Una entrada")
        self.assertEqual(post.get_absolute_url(), f"/post/{post.slug}/")


class ListadoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.publicada = crear_post("Entrada publicada", dias_atras=1)
        cls.borrador = crear_post("Entrada borrador", dias_atras=2, publicado=False)

    def test_el_listado_responde(self):
        respuesta = self.client.get(reverse("blog:lista"))
        self.assertEqual(respuesta.status_code, 200)

    def test_muestra_las_entradas_publicadas(self):
        respuesta = self.client.get(reverse("blog:lista"))
        self.assertContains(respuesta, "Entrada publicada")

    def test_no_muestra_los_borradores(self):
        respuesta = self.client.get(reverse("blog:lista"))
        self.assertNotContains(respuesta, "Entrada borrador")

    def test_muestra_el_extracto(self):
        respuesta = self.client.get(reverse("blog:lista"))
        self.assertContains(respuesta, "Extracto de Entrada publicada")


class PaginacionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        for numero in range(1, 7):
            crear_post(f"Entrada numero {numero}", dias_atras=numero)

    def test_las_cinco_mas_nuevas_estan_en_la_primera_pagina(self):
        respuesta = self.client.get(reverse("blog:lista"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.context["page_obj"].object_list), 5)
        self.assertContains(respuesta, "Entrada numero 1")

    def test_la_segunda_pagina_tiene_la_ultima_entrada(self):
        respuesta = self.client.get(reverse("blog:lista") + "?page=2")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.context["page_obj"].object_list), 1)
        self.assertContains(respuesta, "Entrada numero 6")

    def test_una_pagina_que_no_existe_da_404(self):
        respuesta = self.client.get(reverse("blog:lista") + "?page=99")
        self.assertEqual(respuesta.status_code, 404)


class DetalleTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = crear_post("Entrada para leer")
        cls.borrador = crear_post("Borrador escondido", publicado=False)

    def test_el_detalle_muestra_la_entrada(self):
        respuesta = self.client.get(self.post.get_absolute_url())
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Entrada para leer")
        self.assertContains(respuesta, "Contenido de Entrada para leer")

    def test_los_borradores_no_se_pueden_ver(self):
        respuesta = self.client.get(self.borrador.get_absolute_url())
        self.assertEqual(respuesta.status_code, 404)

    def test_una_entrada_inexistente_da_404(self):
        respuesta = self.client.get("/post/que-no-existe/")
        self.assertEqual(respuesta.status_code, 404)

    def test_el_detalle_muestra_el_formulario_de_comentarios(self):
        respuesta = self.client.get(self.post.get_absolute_url())
        self.assertContains(respuesta, "formulario-comentario")


class ComentarioTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = crear_post("Entrada comentable")
        cls.url = reverse("blog:detalle", args=[cls.post.slug])

    def test_un_visitante_puede_comentar_sin_iniciar_sesion(self):
        respuesta = self.client.post(
            self.url,
            {"name": "Luca", "email": "luca@mail.com", "body": "Buenisimo el post"},
        )
        self.assertEqual(respuesta.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)
        comentario = Comment.objects.get()
        self.assertEqual(comentario.name, "Luca")
        self.assertEqual(comentario.post, self.post)

    def test_despues_de_comentar_vuelve_a_la_entrada(self):
        respuesta = self.client.post(
            self.url,
            {"name": "Luca", "email": "luca@mail.com", "body": "Buenisimo el post"},
        )
        self.assertEqual(respuesta.url, self.url)

    def test_un_comentario_con_datos_vacios_no_se_guarda(self):
        respuesta = self.client.post(self.url, {"name": "", "email": "", "body": ""})
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(Comment.objects.count(), 0)

    def test_un_email_invalido_no_se_guarda(self):
        respuesta = self.client.post(
            self.url, {"name": "Ana", "email": "no-es-un-email", "body": "Hola"}
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(Comment.objects.count(), 0)

    def test_el_comentario_se_muestra_en_la_pagina(self):
        Comment.objects.create(
            post=self.post, name="Nacho", email="nacho@mail.com", body="Muy buen trabajo"
        )
        respuesta = self.client.get(self.url)
        self.assertContains(respuesta, "Nacho")
        self.assertContains(respuesta, "Muy buen trabajo")

    def test_el_formulario_valido_esta_bien_armado(self):
        formulario = CommentForm(
            data={"name": "Ana", "email": "ana@mail.com", "body": "Hola"}
        )
        self.assertTrue(formulario.is_valid())


class PermisosTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = crear_post("Entrada de prueba")
        cls.admin = User.objects.create_superuser("admin", "admin@mail.com", "admin12345")
        cls.visitante = User.objects.create_user(
            "visitante", "visita@mail.com", "visita12345"
        )

    def test_sin_login_lo_manda_al_login(self):
        respuesta = self.client.get(reverse("blog:crear"))
        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(respuesta.url.startswith("/admin/login/"))

    def test_un_usuario_normal_no_puede_crear_entradas(self):
        self.client.force_login(self.visitante)
        respuesta = self.client.get(reverse("blog:crear"))
        self.assertEqual(respuesta.status_code, 403)

    def test_el_admin_puede_ver_el_formulario(self):
        self.client.force_login(self.admin)
        respuesta = self.client.get(reverse("blog:crear"))
        self.assertEqual(respuesta.status_code, 200)

    def test_el_admin_puede_crear_una_entrada(self):
        self.client.force_login(self.admin)
        respuesta = self.client.post(
            reverse("blog:crear"),
            {
                "title": "Entrada nueva",
                "excerpt": "Resumen corto",
                "content": "Texto de la entrada",
                "published": "on",
                "published_at": "2026-10-07T21:00",
            },
        )
        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(Post.objects.filter(title="Entrada nueva").exists())

    def test_un_usuario_normal_no_puede_editar_ni_borrar(self):
        self.client.force_login(self.visitante)
        editar = self.client.get(reverse("blog:editar", args=[self.post.slug]))
        borrar = self.client.get(reverse("blog:borrar", args=[self.post.slug]))
        self.assertEqual(editar.status_code, 403)
        self.assertEqual(borrar.status_code, 403)

    def test_el_admin_puede_editar_una_entrada(self):
        self.client.force_login(self.admin)
        respuesta = self.client.post(
            reverse("blog:editar", args=[self.post.slug]),
            {
                "title": "Entrada de prueba",
                "excerpt": "Extracto editado",
                "content": "Texto de la entrada",
                "published": "on",
                "published_at": "2026-10-07T21:00",
            },
        )
        self.assertEqual(respuesta.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.excerpt, "Extracto editado")

    def test_el_admin_puede_borrar_una_entrada(self):
        self.client.force_login(self.admin)
        respuesta = self.client.post(reverse("blog:borrar", args=[self.post.slug]))
        self.assertEqual(respuesta.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

    def test_sin_login_no_puede_editar(self):
        respuesta = self.client.get(reverse("blog:editar", args=[self.post.slug]))
        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(respuesta.url.startswith("/admin/login/"))


class PortfolioTests(TestCase):
    def test_el_portfolio_responde(self):
        respuesta = self.client.get(reverse("pages:portfolio"))
        self.assertEqual(respuesta.status_code, 200)

    def test_el_portfolio_tiene_sus_secciones(self):
        respuesta = self.client.get(reverse("pages:portfolio"))
        for seccion in ("sobre-mi", "proyectos", "habilidades", "contacto"):
            self.assertContains(respuesta, f'id="{seccion}"')

    def test_el_nav_lleva_al_blog_y_al_portfolio(self):
        respuesta = self.client.get(reverse("blog:lista"))
        self.assertContains(respuesta, reverse("pages:portfolio"))


class MensajesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser("admin", "admin@mail.com", "admin12345")

    def test_al_crear_una_entrada_aparece_un_mensaje(self):
        self.client.force_login(self.admin)
        respuesta = self.client.post(
            reverse("blog:crear"),
            {
                "title": "Con mensaje",
                "excerpt": "Resumen",
                "content": "Contenido",
                "published": "on",
                "published_at": "2026-10-07T21:00",
            },
            follow=True,
        )
        self.assertContains(respuesta, "La entrada se creo correctamente")
