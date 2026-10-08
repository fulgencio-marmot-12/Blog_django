# Bitácora del trabajo práctico

Sitio web personal con Django: blog + portfolio.
Laboratorio de Algoritmos y Estructuras de Datos — entrega jueves 8 de octubre.

---

## Qué había que hacer

Agregar a mi sitio web personal un blog con entradas ordenadas cronológicamente,
con texto y archivos multimedia, comentarios que pueda borrar el administrador,
y que **solo** el administrador pueda crear entradas. Todo con Django y con una
estética coherente con mi portfolio.

---

## Cómo lo fui haciendo

Fui subiendo avances al repositorio en 9 commits, pensados para que cada uno
deje el proyecto en un estado que funcione:

| Commit | Qué dejó hecho |
| --- | --- |
| `agrego estructura del proyecto django` | proyecto `sitio`, settings con español de Argentina, carpetas `static`, `templates` y `media` |
| `modelo Post con su admin y migraciones` | modelo de entradas con slug automático y el alta desde el panel |
| `comentarios anonimos con su formulario` | modelo `Comment` y el `CommentForm` |
| `vistas del blog con listado, detalle y comentarios` | portada paginada, detalle, y crear/editar/borrar entradas restringido al admin |
| `base html, estilos del portfolio y pagina portfolio` | el `base.html` con el header de mi portfolio, el CSS compartido y la página `/portfolio` |
| `admin personalizado con el titulo del blog` | branding del panel, contador de comentarios e inline de comentarios |
| `tests del blog con django` | 34 tests que cubren listado, permisos, comentarios y paginación |
| `bitacora con las dificultades y como las resolvi` | este archivo |
| `readme con la explicacion del proyecto` | el README del repositorio |

---

## Dificultades que encontré y cómo las resolví

**1. El cliente de prueba rechazaba todas las peticiones (400).**
Al probar las vistas con el `Client` de Django desde el shell, todo volvía
`Invalid HTTP_HOST header: 'testserver'`. Era porque `ALLOWED_HOSTS` estaba
vacío y con `DEBUG = True` Django sólo acepta hosts conocidos. Lo resolví
creando el cliente con `Client(SERVER_NAME='127.0.0.1')`. En los tests
formales no pasa porque Django agrega `testserver` solo.

**2. Editar o borrar una entrada tiraba `ImproperlyConfigured`.**
Al visitar `/post/<slug>/editar/` salía *"PostUpdateView is missing a
QuerySet"*. Me había olvidado de poner `model = Post` en las vistas de
edición y de borrado: como sólo definí `form_class`, Django no sabía de qué
objeto se trataba. Se agregó `model = Post` y quedó funcionando.

**3. Los anónimos recibían 403 en vez de ir al login.**
Primero usé `raise_exception = True` en la mezcla de permisos y eso hacía que
cualquiera sin sesión recibiera un error 403 directo, sin pasar por el login.
Lo cambié sobreescribiendo `handle_no_permission`: si el usuario está logueado
pero no es admin, responde 403; si no tiene sesión, lo manda al login del
panel. Está en `blog/views.py`.

**4. No encontraba las imágenes de mi portfolio.**
Cuando quise copiar `mastacards.png`, `slitherio.png`, el favicon y el CV a
`static/`, vi que no estaban en la carpeta del portfolio (sólo quedaban el
HTML y el CSS). No las encontré en ningún lado de Documentos. Mientras tanto:
- dejé todas las rutas preparadas en los templates (`{% static %}`),
- creé un `favicon.svg` con el mismo estilo de caja con borde que mi portfolio.
Lo que falta es copiar los archivos a `static/img/` y el CV a `static/`.

**5. `ImageField` no andaba sin Pillow.**
La primera vez que probé subir una imagen tiraba que faltaba la librería de
imágenes. Se resolvió instalando Pillow y dejándolo en el `requirements.txt`.

**6. El `.gitignore` no cubría las subidas.**
Como las fotos de las entradas se guardan en `media/`, y eso no estaba en el
`.gitignore`, cualquier foto iba a terminar subida al repo. Agregué `media/` y
`staticfiles/`.

**7. Pensé que el borrado de comentarios no funcionaba.**
Al probar la acción de borrar desde el panel devolvía 200 en vez de un 302 y
me pareció que no había pasado nada. Era la pantalla de confirmación que
muestra Django por defecto; al confirmar (`post=yes`) borra bien. Probado con
y sin inline.

**8. Caracteres raros en los archivos de la guía.**
Los markdown de mi tutorial anterior se habían guardado con codificación mal
y en GitHub se veían signos de interrogación. Por eso escribí todos los
archivos nuevos en UTF-8.

---

## Qué hubiera hecho distinto

- **Empezar con las dos apps y el `base.html` de una**, en vez de sumar el
  portfolio al final: me hizo reescribir el header dos veces.
- **Poner `ALLOWED_HOSTS` desde el principio** y no enterarme por los 400.
- **Escribir los tests mientras hacía cada vista**, no todos juntos al final.
  Me habrían ahorrado el problema de los permisos y el del `model = Post`,
  que los detecté recién al probar a mano.
- **Pensar mejor la app `pages`**: hoy tiene una sola vista (el portfolio).
  Si en algún momento quería sumar más páginas sueltas, mejor lo preveía desde
  el principio en vez de dejar una app casi vacía.
- **No confiar en que las imágenes estaban en la carpeta del portfolio**: lo
  ideal era subirlas al repo apenas las hice.

---

## Qué me quedó en el tintero

- **Registro e inicio de sesión para los que comentan.** El trabajo lo deja a
  nuestra elección; elegí comentarios anónimos con nombre y email porque es
  lo más simple y no pedía más. Con `django.contrib.auth` se podría sumar.
- **Notificación por email cuando entra un comentario**, para que el admin no
  tenga que entrar al panel a mirar.
- **Categorías o etiquetas** para agrupar entradas y un buscador
  (`django.contrib.postgres` o un filtro simple en el listado).
- **Editor con Markdown o enriquecido** para escribir las entradas, en vez de
  texto plano.
- **Varias imágenes por entrada** (una galería), hoy sólo entra una.
- **Tags o archivo por mes** en el blog, como en los ejemplos del enunciado.
- **Subir el sitio a internet** (Render, PythonAnywhere o Railway) para que
  se pueda ver en vivo, con `DEBUG = 0` y un `SECRET_KEY` de variable de
  entorno.
- **Feeds RSS y sitemap**, y quizás comentarios con aprobación previa.
- **Personalizar más el panel** (portada con estadísticas, ver los borradores
  con un badge).

---

## Cómo se ejecuta

```powershell
# desde la carpeta del proyecto
git clone https://github.com/fulgencio-marmot-12/Blog_django.git
cd Blog_django

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- <http://127.0.0.1:8000/> → el blog
- <http://127.0.0.1:8000/portfolio/> → mi portfolio
- <http://127.0.0.1:8000/admin/> → panel de administración

Los tests: `python manage.py test blog`.
