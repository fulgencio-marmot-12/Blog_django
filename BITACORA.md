# la biracora del trabajo


## Como lo hice

Fui subiendo avances al repositorio en maso menos 20 comits. En estos especifico que hago que cambio y para que.
---

## Cómo se ejecuta

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

- <http://127.0.0.1:8000/> → el blog
- <http://127.0.0.1:8000/portfolio/> → mi portfolio
- <http://127.0.0.1:8000/admin/> → panel de administración

