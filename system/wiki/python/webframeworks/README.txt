# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: Flask/Django/FastAPI Dokumentation, Real Python, TestDriven.io

WEB-FRAMEWORKS IN PYTHON
========================

Stand: 2026-02-05

UEBERBLICK
==========
  Python bietet erstklassige Web-Frameworks fuer jede Projektgroesse.
  Von Microframeworks bis zu Full-Stack-Loesungen.

  Die drei wichtigsten Frameworks:
    - Flask: Microframework, flexibel, leichtgewichtig
    - Django: Full-Stack, "Batteries included"
    - FastAPI: Modern, async, API-first

FLASK - DAS MICROFRAMEWORK
==========================

  KONZEPT
  -------
    - Minimalistisch: Nur das Noetigste
    - Erweiterbar durch Extensions
    - Volle Kontrolle ueber Architektur
    - WSGI-basiert

  INSTALLATION
  ------------
    pip install flask

  HELLO WORLD
  -----------
    from flask import Flask

    app = Flask(__name__)

    @app.route('/')
    def hello():
        return 'Hallo Welt!'

    if __name__ == '__main__':
        app.run(debug=True)

  ROUTING
  -------
    @app.route('/user/<username>')
    def show_user(username):
        return f'Benutzer: {username}'

    @app.route('/post/<int:post_id>')
    def show_post(post_id):
        return f'Post ID: {post_id}'

    # HTTP-Methoden
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            return do_login()
        return show_login_form()

  TEMPLATES (JINJA2)
  ------------------
    # app.py
    from flask import render_template

    @app.route('/hello/<name>')
    def hello(name):
        return render_template('hello.html', name=name)

    # templates/hello.html
    <!DOCTYPE html>
    <html>
      <body>
        <h1>Hallo {{ name }}!</h1>
      </body>
    </html>

  WICHTIGE EXTENSIONS
  -------------------
    Flask-SQLAlchemy    ORM/Datenbank
    Flask-Login         Authentifizierung
    Flask-WTF           Formulare
    Flask-Migrate       Datenbank-Migrationen
    Flask-RESTful       REST APIs
    Flask-CORS          Cross-Origin Requests

  WANN FLASK?
  -----------
    - Kleine bis mittlere Projekte
    - APIs und Microservices
    - Prototypen und MVPs
    - Wenn volle Kontrolle gewuenscht

DJANGO - DAS FULL-STACK FRAMEWORK
=================================

  KONZEPT
  -------
    - "Batteries included" - alles dabei
    - MTV-Pattern (Model-Template-View)
    - Admin-Interface out-of-the-box
    - ORM integriert
    - Security-Features eingebaut

  INSTALLATION
  ------------
    pip install django

  PROJEKT ERSTELLEN
  -----------------
    django-admin startproject meinprojekt
    cd meinprojekt
    python manage.py startapp meine_app

  PROJEKTSTRUKTUR
  ---------------
    meinprojekt/
      manage.py
      meinprojekt/
        __init__.py
        settings.py      Konfiguration
        urls.py          URL-Routing
        wsgi.py          WSGI-Entry
      meine_app/
        models.py        Datenmodelle
        views.py         View-Funktionen
        urls.py          App-URLs
        admin.py         Admin-Konfiguration
        templates/       HTML-Templates

  MODELS (ORM)
  ------------
    # models.py
    from django.db import models

    class Artikel(models.Model):
        titel = models.CharField(max_length=200)
        inhalt = models.TextField()
        erstellt = models.DateTimeField(auto_now_add=True)
        veroeffentlicht = models.BooleanField(default=False)

        def __str__(self):
            return self.titel

  VIEWS
  -----
    # views.py - Function-Based View
    from django.shortcuts import render, get_object_or_404
    from .models import Artikel

    def artikel_liste(request):
        artikel = Artikel.objects.filter(veroeffentlicht=True)
        return render(request, 'artikel/liste.html', {'artikel': artikel})

    # Class-Based View
    from django.views.generic import ListView

    class ArtikelListView(ListView):
        model = Artikel
        template_name = 'artikel/liste.html'
        context_object_name = 'artikel'

  URL-ROUTING
  -----------
    # urls.py
    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.artikel_liste, name='artikel-liste'),
        path('<int:pk>/', views.artikel_detail, name='artikel-detail'),
    ]

  ADMIN-INTERFACE
  ---------------
    # admin.py
    from django.contrib import admin
    from .models import Artikel

    @admin.register(Artikel)
    class ArtikelAdmin(admin.ModelAdmin):
        list_display = ['titel', 'erstellt', 'veroeffentlicht']
        list_filter = ['veroeffentlicht', 'erstellt']
        search_fields = ['titel', 'inhalt']

  WANN DJANGO?
  ------------
    - Grosse, komplexe Projekte
    - Content-Management-Systeme
    - E-Commerce-Plattformen
    - Wenn Admin-Interface benoetigt
    - Teams mit Django-Erfahrung

FASTAPI - DAS MODERNE API-FRAMEWORK
===================================

  KONZEPT
  -------
    - Async-first (ASGI)
    - Automatische API-Dokumentation
    - Type Hints fuer Validierung
    - Hoechste Performance
    - Pydantic fuer Datenvalidierung

  INSTALLATION
  ------------
    pip install fastapi uvicorn

  HELLO WORLD
  -----------
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    async def root():
        return {"message": "Hallo Welt!"}

    # Starten: uvicorn main:app --reload

  AUTOMATISCHE DOKUMENTATION
  --------------------------
    Nach Start verfuegbar unter:
      http://localhost:8000/docs       Swagger UI
      http://localhost:8000/redoc      ReDoc

  PATH PARAMETER UND TYPE HINTS
  -----------------------------
    from fastapi import FastAPI, Path, Query

    @app.get("/items/{item_id}")
    async def get_item(
        item_id: int = Path(..., title="Die Item ID", ge=1),
        q: str | None = Query(None, max_length=50)
    ):
        return {"item_id": item_id, "q": q}

  REQUEST BODY MIT PYDANTIC
  -------------------------
    from pydantic import BaseModel

    class Item(BaseModel):
        name: str
        preis: float
        beschreibung: str | None = None
        auf_lager: bool = True

    @app.post("/items/")
    async def create_item(item: Item):
        return item

  ASYNC/AWAIT
  -----------
    import httpx

    @app.get("/external-api")
    async def call_external():
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.example.com/data")
            return response.json()

  DEPENDENCY INJECTION
  --------------------
    from fastapi import Depends

    async def get_db():
        db = Database()
        try:
            yield db
        finally:
            db.close()

    @app.get("/users/")
    async def get_users(db = Depends(get_db)):
        return db.get_all_users()

  WANN FASTAPI?
  -------------
    - REST APIs und Microservices
    - Async-Anwendungen
    - ML/AI API-Endpoints
    - Wenn Performance kritisch
    - Moderne Python-Projekte (3.8+)

FRAMEWORK-VERGLEICH
===================

  | Kriterium        | Flask      | Django     | FastAPI    |
  |------------------|------------|------------|------------|
  | Lernkurve        | Niedrig    | Mittel     | Niedrig    |
  | Performance      | Mittel     | Mittel     | Hoch       |
  | Async Support    | Limited    | Partial    | Native     |
  | ORM              | Extension  | Integriert | External   |
  | Admin UI         | Extension  | Integriert | External   |
  | API Docs         | Extension  | Extension  | Integriert |
  | Community        | Gross      | Sehr gross | Wachsend   |
  | Projektgroesse   | Klein-M    | Mittel-XL  | Klein-L    |

DEPLOYMENT
==========

  FLASK
  -----
    # Gunicorn (Production)
    pip install gunicorn
    gunicorn -w 4 app:app

  DJANGO
  ------
    # Gunicorn + Nginx
    pip install gunicorn
    gunicorn meinprojekt.wsgi:application

  FASTAPI
  -------
    # Uvicorn (Production)
    pip install uvicorn[standard]
    uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

BEST PRACTICES
==============
  1. Virtuelle Umgebung nutzen (venv/poetry/pipenv)
  2. Environment Variables fuer Secrets
  3. requirements.txt oder pyproject.toml pflegen
  4. Logging konfigurieren
  5. Tests schreiben (pytest)
  6. CORS korrekt konfigurieren
  7. Rate Limiting implementieren
  8. HTTPS in Production erzwingen

SICHERHEIT
==========
  - CSRF-Schutz aktivieren
  - SQL-Injection vermeiden (ORM nutzen)
  - XSS verhindern (Template-Escaping)
  - Secrets nicht im Code
  - Dependency-Updates regelmaessig
  - Input-Validierung konsequent

BACH-INTEGRATION
================
  Partner-Zuweisung:
    - Claude: Code-Review, Architektur-Beratung
    - Gemini: Aktuelle Framework-Updates recherchieren
    - Ollama: Lokale API-Tests

  Typische Aufgaben:
    - API-Endpoints generieren
    - Models/Schemas erstellen
    - Tests schreiben
    - Deployment-Configs

SIEHE AUCH
==========
  wiki/python/README.txt
  wiki/webapps/README.txt
  wiki/webapps/testing/README.txt
  wiki/informatik/devops/README.txt
