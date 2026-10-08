# Blog_django

Sitio web personal hecho con **Django**: un blog con entradas y comentarios,
más mi portfolio, todo con la misma estética (mismo CSS, mismas tipografías y
modo oscuro).

Trabajo práctico de *Laboratorio de Algoritmos y Estructuras de Datos*.

## Qué tiene

- **Blog** en la portada: entradas ordenadas de más nueva a más vieja, con
  imagen, extracto, texto y paginación (5 por página).
- **Comentarios anónimos** en cada entrada (nombre, email y texto). No hace
  falta registrarse y los borra el administrador desde el panel.
- **Sólo el administrador** puede crear, editar y borrar entradas: desde el
  sitio (`/post/nuevo/`) o desde `/admin/`. Cualquier visitante manda al login
  y un usuario sin permisos recibe un 403.
- **Portfolio** en `/portfolio`, con las mismas secciones del sitio original:
  sobre mí, proyectos, habilidades y contacto.
- **Modo oscuro** con el mismo botón del portfolio, que recuerda la
  preferencia en el navegador.
- **Panel de administración** personalizado: entradas con contador de
  comentarios, filtros, búsqueda y los comentarios de cada entrada en línea.
- **34 tests** que cubren listado, paginación, permisos, comentarios y el
  portfolio.

## Cómo ejecutarlo

```powershell
git clone https://github.com/fulgencio-marmot-12/Blog_django.git
cd Blog_django

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

| URL | Qué muestra |
| --- | --- |
| <http://127.0.0.1:8000/> | el blog |
| <http://127.0.0.1:8000/portfolio/> | el portfolio |
| <http://127.0.0.1:8000/admin/> | panel de administración |
| <http://127.0.0.1:8000/post/nuevo/> | crear una entrada (sólo admin) |

Para correr los tests: `python manage.py test blog`.

## Estructura

```
Blog_django/
├── sitio/                 configuración del proyecto (settings, urls)
├── blog/                  entradas, comentarios, vistas, forms, tests
├── pages/                 página del portfolio
├── templates/             base.html y branding del admin
├── static/css/styles.css  estilos compartidos con el portfolio
├── static/img/            imágenes del portfolio y favicon
├── media/                 fotos que sube el administrador (no se sube al repo)
├── BITACORA.md            dificultades, resoluciones y pendientes
└── requirements.txt       dependencias exactas
```

## Para terminar de completar

Falta copiar a `static/img/` los archivos del portfolio original
(`mastacards.png`, `slitherio.png`) y el CV a `static/`
(`CV_Facundo_Saint_Martin_ATS.pdf`). Las rutas ya están preparadas en los
templates. Las fotos de cada entrada se suben desde el panel y quedan en
`media/posts/`.

## Tecnologías

Django 6.1.2 · Python 3.13 · SQLite · HTML · CSS · Font Awesome · Google Fonts

Más detalles en [BITACORA.md](BITACORA.md).
