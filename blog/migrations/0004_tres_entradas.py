"""Crea las tres entradas del blog con sus imagenes."""

from datetime import datetime

from django.db import migrations
from django.utils.timezone import make_aware

ENTRADAS = [
    {
        "title": "Un domingo en La Boca: Caminito, choripán y remeras",
        "slug": "un-domingo-en-la-boca-caminito-choripan-y-remeras",
        "excerpt": (
            "Un paseo por Caminito con mi familia, choripán en la vereda y "
            "dos remeras de Boca de regreso. Un domingo simple, con el barrio "
            "lleno de color."
        ),
        "content": (
            "La verdad es que hacía rato que quería volver a La Boca, y esta "
            "vez agarré y propuse la salida con mi familia. Fue un domingo a "
            "la mañana, temprano, antes de que se llene de verdad.\n\n"
            "Caminito se recorre despacio. Las casas de colores, los faroles "
            "viejos, los artistas en la vereda vendiendo sus cosas. Nos "
            "sacamos fotos en todas las esquinas, como turistas en nuestro "
            "propio barrio, y nadie se quejó.\n\n"
            "A la hora del almuerzo no lo pensamos dos veces: choripán. Nos "
            "sentamos en la vereda con el pan caliente y el chimichurri de "
            "más, que es medio la definición de un buen domingo.\n\n"
            "Antes de volver pasé por un puesto de remeras y me compré dos de "
            "Boca. Las que llevaba mirando hace rato, las del azul y oro que "
            "quedan con todo. Mi vieja hizo el comentario de siempre, pero "
            "después de mirarlas un rato hasta ella admitió que estaban "
            "buenas.\n\n"
            "Un día corto, de esos que no necesitan nada más: familia, comer "
            "bien y volver a casa con una bolsa de más."
        ),
        "image": "posts/caminito-la-boca.webp",
        "fecha": (2026, 9, 20, 19, 0),
    },
    {
        "title": "Una vuelta en bici por Puerto Madero",
        "slug": "una-vuelta-en-bici-por-puerto-madero",
        "excerpt": (
            "Una mañana en bici por Puerto Madero: mate con mi vieja y mis "
            "amigos, música en los oídos y más de un conocido cruzado en el "
            "camino."
        ),
        "content": (
            "Agarré la bici un sábado con la idea de dar una vuelta por "
            "Puerto Madero y, como casi siempre, el plan creció en el "
            "camino. Salieron mi vieja, se sumaron unos amigos y fuimos "
            "bajando por la costera hasta la reserva.\n\n"
            "En algún punto paramos a tomar mate en un banco, con el río de "
            "fondo y sin apuro por ningún lado. Eso es lo bueno de salir en "
            "bici: nadie mira el reloj.\n\n"
            "En el camino me crucé con dos o tres conocidos, el saludo "
            "típico de “che, ¿qué hacés acá?”, unas charlas cortas "
            "y seguimos. Y con la música de fondo en los auriculares, el "
            "ritmo lo ponía la pedalada.\n\n"
            "Llegué a casa con las piernas cargadas pero con la cabeza bien "
            "despejada. Vale la pena repetirlo."
        ),
        "image": "posts/bicicleta-puerto-madero.jpg",
        "fecha": (2026, 10, 3, 17, 0),
    },
    {
        "title": "Shawarma en Monserrat con mis padres",
        "slug": "shawarma-en-monserrat-con-mis-padres",
        "excerpt": (
            "Una noche de shawarma por Monserrat con mis padres, cosas para "
            "compartir en el medio de la mesa y una charla que se alargó "
            "hasta que cerraron."
        ),
        "content": (
            "Una noche aprovechamos que estábamos los tres y salimos a cenar "
            "por Monserrat: mi vieja, mi viejo y yo, con unas ganas de "
            "shawarma que veníamos arrastrando hace semanas.\n\n"
            "El local es chiquito y siempre lleno, así que pedimos mesa con "
            "tiempo. Pedimos para compartir entre todos: un par de shawarmas "
            "para arrancar, cosas para picar en el medio de la mesa y salsas "
            "de más. La verdad es que no sobró nada.\n\n"
            "La comida estaba buenísima y la charla todavía mejor, de todo un "
            "poco como siempre que nos juntamos a comer, hasta que cerraron y "
            "nos quedamos un rato hablando en la puerta.\n\n"
            "Volvimos a casa con la panza llena y la sensación de que hay que "
            "salir a comer así más seguido."
        ),
        "image": "posts/shawarma-en-monserrat.jpg",
        "fecha": (2026, 10, 5, 22, 0),
    },
]


def crear_entradas(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    for entrada in ENTRADAS:
        anio, mes, dia, hora, minuto = entrada["fecha"]
        defaults = {
            "title": entrada["title"],
            "excerpt": entrada["excerpt"],
            "content": entrada["content"],
            "image": entrada["image"],
            "published": True,
            "published_at": make_aware(datetime(anio, mes, dia, hora, minuto)),
        }
        Post.objects.get_or_create(slug=entrada["slug"], defaults=defaults)


def borrar_entradas(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    Post.objects.filter(slug__in=[e["slug"] for e in ENTRADAS]).delete()


class Migration(migrations.Migration):
    dependencies = [("blog", "0003_alter_post_title")]

    operations = [migrations.RunPython(crear_entradas, borrar_entradas)]
