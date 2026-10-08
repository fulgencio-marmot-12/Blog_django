# Blog_django

Sitio web personal hecho con el framework **Django** de python donde cuanto cosas de mi vida.

Trabajo práctico de *Laboratorio de Algoritmos y Estructuras de Datos*.

## Que tiene el proyecto

- **Blog**
- **Comentarios anónimos** 
- **Sólo el administrador**
- **Portfolio** 
- **Modo oscuro**
- **Panel de administración**

## Como ejecutarlo

Desde la consola ejecuta los siguientes comandos paso a paso.
```powershell
git clone https://github.com/fulgencio-marmot-12/Blog_django.git
cd Blog_django

python -m pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Si preferis aislar todo en un entorno virtual (opcional):

```powershell
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


## Tecnologias

Django 6.1.2 · Python 3.13 · SQLite · HTML · CSS · Font Awesome · Google Fonts

Más detalles en [BITACORA.md](BITACORA.md).
