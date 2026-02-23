# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: fastapi.tiangolo.com, flask.palletsprojects.com,
#          docs.pydantic.dev, swagger.io/specification,
#          restfulapi.net, Real Python

API-ENTWICKLUNG MIT PYTHON
==========================

Stand: 2026-02-05

UEBERBLICK
==========
  APIs (Application Programming Interfaces) ermoeglichen
  Kommunikation zwischen Software-Komponenten. REST APIs
  sind der verbreiteste Standard fuer Web-Services.

  Beliebte Python-Frameworks:
  - FastAPI: Modern, schnell, automatische Docs
  - Flask: Leichtgewichtig, flexibel
  - Django REST Framework: Vollstaendig, Enterprise

REST GRUNDLAGEN
===============

HTTP METHODEN
-------------
  GET     Daten abrufen           /users/123
  POST    Neue Ressource erstellen /users
  PUT     Ressource ersetzen       /users/123
  PATCH   Ressource teilweise aendern /users/123
  DELETE  Ressource loeschen       /users/123

STATUSCODES
-----------
  2xx Erfolg:
    200 OK                  Anfrage erfolgreich
    201 Created             Ressource erstellt
    204 No Content          Erfolgreich, keine Daten

  4xx Client-Fehler:
    400 Bad Request         Ungueltige Anfrage
    401 Unauthorized        Authentifizierung fehlt
    403 Forbidden           Keine Berechtigung
    404 Not Found           Ressource nicht gefunden
    422 Unprocessable       Validierungsfehler

  5xx Server-Fehler:
    500 Internal Error      Serverfehler
    503 Service Unavailable Server ueberlastet

FASTAPI (EMPFOHLEN)
===================

INSTALLATION
------------
  pip install fastapi uvicorn[standard]

MINIMALE API
------------
  # main.py
  from fastapi import FastAPI

  app = FastAPI(
      title="Meine API",
      description="Beispiel-API mit FastAPI",
      version="1.0.0"
  )

  @app.get("/")
  async def root():
      return {"message": "Hallo Welt"}

  @app.get("/items/{item_id}")
  async def read_item(item_id: int):
      return {"item_id": item_id}

  # Starten: uvicorn main:app --reload

PYDANTIC MODELS
---------------
  from pydantic import BaseModel, Field, EmailStr
  from typing import Optional
  from datetime import datetime

  class UserBase(BaseModel):
      email: EmailStr
      name: str = Field(..., min_length=2, max_length=50)

  class UserCreate(UserBase):
      password: str = Field(..., min_length=8)

  class UserResponse(UserBase):
      id: int
      created_at: datetime
      is_active: bool = True

      class Config:
          from_attributes = True  # Fuer ORM-Kompatibilitaet

CRUD OPERATIONEN
----------------
  from fastapi import FastAPI, HTTPException, status
  from typing import List

  app = FastAPI()

  # Simulierte Datenbank
  users_db: dict[int, dict] = {}
  next_id = 1

  @app.post("/users/", response_model=UserResponse,
            status_code=status.HTTP_201_CREATED)
  async def create_user(user: UserCreate):
      global next_id
      user_dict = user.model_dump()
      user_dict["id"] = next_id
      user_dict["created_at"] = datetime.now()
      users_db[next_id] = user_dict
      next_id += 1
      return user_dict

  @app.get("/users/", response_model=List[UserResponse])
  async def list_users(skip: int = 0, limit: int = 10):
      return list(users_db.values())[skip:skip + limit]

  @app.get("/users/{user_id}", response_model=UserResponse)
  async def get_user(user_id: int):
      if user_id not in users_db:
          raise HTTPException(
              status_code=status.HTTP_404_NOT_FOUND,
              detail=f"User {user_id} nicht gefunden"
          )
      return users_db[user_id]

  @app.put("/users/{user_id}", response_model=UserResponse)
  async def update_user(user_id: int, user: UserCreate):
      if user_id not in users_db:
          raise HTTPException(status_code=404, detail="Not found")
      users_db[user_id].update(user.model_dump())
      return users_db[user_id]

  @app.delete("/users/{user_id}", status_code=204)
  async def delete_user(user_id: int):
      if user_id not in users_db:
          raise HTTPException(status_code=404)
      del users_db[user_id]

QUERY PARAMETER
---------------
  @app.get("/items/")
  async def list_items(
      skip: int = 0,
      limit: int = 10,
      search: Optional[str] = None,
      active: bool = True
  ):
      # /items/?skip=10&limit=20&search=test&active=false
      return {"skip": skip, "limit": limit,
              "search": search, "active": active}

REQUEST BODY + PATH
-------------------
  @app.put("/items/{item_id}")
  async def update_item(
      item_id: int,                    # Path Parameter
      item: ItemUpdate,                # Request Body
      q: Optional[str] = None          # Query Parameter
  ):
      return {"item_id": item_id, "item": item, "q": q}

DEPENDENCY INJECTION
====================

GRUNDLAGEN
----------
  from fastapi import Depends

  def get_db():
      db = DatabaseSession()
      try:
          yield db
      finally:
          db.close()

  def get_current_user(token: str = Header(...)):
      user = verify_token(token)
      if not user:
          raise HTTPException(status_code=401)
      return user

  @app.get("/profile")
  async def profile(
      db: Session = Depends(get_db),
      user: User = Depends(get_current_user)
  ):
      return {"user": user.name}

AUTHENTIFIZIERUNG
=================

JWT TOKEN
---------
  from fastapi import Depends, HTTPException
  from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
  from jose import JWTError, jwt
  from datetime import datetime, timedelta

  SECRET_KEY = "geheimer-schluessel"
  ALGORITHM = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES = 30

  oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

  def create_access_token(data: dict):
      to_encode = data.copy()
      expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
      to_encode.update({"exp": expire})
      return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

  async def get_current_user(token: str = Depends(oauth2_scheme)):
      try:
          payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
          username: str = payload.get("sub")
          if username is None:
              raise HTTPException(status_code=401)
      except JWTError:
          raise HTTPException(status_code=401)
      return username

  @app.post("/token")
  async def login(form_data: OAuth2PasswordRequestForm = Depends()):
      # Benutzer verifizieren...
      access_token = create_access_token(data={"sub": form_data.username})
      return {"access_token": access_token, "token_type": "bearer"}

  @app.get("/protected")
  async def protected_route(user: str = Depends(get_current_user)):
      return {"user": user}

API KEY
-------
  from fastapi.security import APIKeyHeader

  api_key_header = APIKeyHeader(name="X-API-Key")

  async def verify_api_key(api_key: str = Depends(api_key_header)):
      if api_key != "geheimer-api-key":
          raise HTTPException(status_code=403)
      return api_key

  @app.get("/secure", dependencies=[Depends(verify_api_key)])
  async def secure_endpoint():
      return {"status": "authenticated"}

FEHLERBEHANDLUNG
================

CUSTOM EXCEPTIONS
-----------------
  from fastapi import FastAPI, HTTPException
  from fastapi.responses import JSONResponse

  class CustomException(Exception):
      def __init__(self, name: str, code: int):
          self.name = name
          self.code = code

  @app.exception_handler(CustomException)
  async def custom_exception_handler(request, exc: CustomException):
      return JSONResponse(
          status_code=exc.code,
          content={"error": exc.name, "detail": "Custom error occurred"}
      )

  @app.get("/fail")
  async def trigger_error():
      raise CustomException(name="TestError", code=418)

VALIDATION ERRORS
-----------------
  from fastapi.exceptions import RequestValidationError
  from fastapi.responses import JSONResponse

  @app.exception_handler(RequestValidationError)
  async def validation_exception_handler(request, exc):
      return JSONResponse(
          status_code=422,
          content={
              "error": "Validation Error",
              "details": exc.errors()
          }
      )

MIDDLEWARE
==========

CORS
----
  from fastapi.middleware.cors import CORSMiddleware

  app.add_middleware(
      CORSMiddleware,
      allow_origins=["http://localhost:3000", "https://meine-app.de"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )

CUSTOM MIDDLEWARE
-----------------
  from fastapi import Request
  import time

  @app.middleware("http")
  async def add_process_time_header(request: Request, call_next):
      start_time = time.time()
      response = await call_next(request)
      process_time = time.time() - start_time
      response.headers["X-Process-Time"] = str(process_time)
      return response

LOGGING MIDDLEWARE
------------------
  import logging

  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)

  @app.middleware("http")
  async def log_requests(request: Request, call_next):
      logger.info(f"{request.method} {request.url}")
      response = await call_next(request)
      logger.info(f"Status: {response.status_code}")
      return response

DATENBANKANBINDUNG
==================

SQLALCHEMY (ASYNC)
------------------
  from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
  from sqlalchemy.orm import sessionmaker, declarative_base

  DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/db"

  engine = create_async_engine(DATABASE_URL)
  async_session = sessionmaker(engine, class_=AsyncSession)
  Base = declarative_base()

  async def get_db():
      async with async_session() as session:
          yield session

MODEL DEFINITION
----------------
  from sqlalchemy import Column, Integer, String, DateTime
  from datetime import datetime

  class User(Base):
      __tablename__ = "users"

      id = Column(Integer, primary_key=True, index=True)
      email = Column(String, unique=True, index=True)
      name = Column(String)
      hashed_password = Column(String)
      created_at = Column(DateTime, default=datetime.utcnow)

CRUD MIT DB
-----------
  from sqlalchemy import select
  from sqlalchemy.ext.asyncio import AsyncSession

  async def create_user(db: AsyncSession, user: UserCreate):
      db_user = User(**user.model_dump())
      db.add(db_user)
      await db.commit()
      await db.refresh(db_user)
      return db_user

  async def get_user(db: AsyncSession, user_id: int):
      result = await db.execute(select(User).where(User.id == user_id))
      return result.scalar_one_or_none()

TESTING
=======

PYTEST MIT FASTAPI
------------------
  # test_api.py
  import pytest
  from httpx import AsyncClient
  from main import app

  @pytest.mark.asyncio
  async def test_create_user():
      async with AsyncClient(app=app, base_url="http://test") as client:
          response = await client.post(
              "/users/",
              json={"email": "test@test.de", "name": "Test", "password": "12345678"}
          )
      assert response.status_code == 201
      assert response.json()["email"] == "test@test.de"

  @pytest.mark.asyncio
  async def test_get_user_not_found():
      async with AsyncClient(app=app, base_url="http://test") as client:
          response = await client.get("/users/999")
      assert response.status_code == 404

TEST CLIENT SYNC
----------------
  from fastapi.testclient import TestClient

  client = TestClient(app)

  def test_read_root():
      response = client.get("/")
      assert response.status_code == 200
      assert response.json() == {"message": "Hallo Welt"}

DOKUMENTATION
=============

AUTOMATISCHE DOCS
-----------------
  FastAPI generiert automatisch:
  - Swagger UI:    http://localhost:8000/docs
  - ReDoc:         http://localhost:8000/redoc
  - OpenAPI JSON:  http://localhost:8000/openapi.json

DOCSTRINGS NUTZEN
-----------------
  @app.post("/users/",
            summary="Neuen Benutzer erstellen",
            description="Erstellt einen neuen Benutzer in der Datenbank.",
            response_description="Der erstellte Benutzer")
  async def create_user(user: UserCreate):
      """
      Erstellt einen neuen Benutzer mit folgenden Informationen:

      - **email**: Gueltige E-Mail-Adresse
      - **name**: Name des Benutzers (2-50 Zeichen)
      - **password**: Passwort (mindestens 8 Zeichen)
      """
      pass

TAGS FUER GRUPPIERUNG
---------------------
  from fastapi import APIRouter

  router = APIRouter(prefix="/users", tags=["users"])

  @router.get("/")
  async def list_users():
      pass

  @router.post("/")
  async def create_user():
      pass

  app.include_router(router)

DEPLOYMENT
==========

UVICORN PRODUCTION
------------------
  # Mit mehreren Workern:
  uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

  # Mit Gunicorn (empfohlen fuer Production):
  pip install gunicorn
  gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

DOCKER
------
  # Dockerfile
  FROM python:3.11-slim

  WORKDIR /app

  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt

  COPY . .

  EXPOSE 8000

  CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

BEST PRACTICES
==============

PROJEKT-STRUKTUR
----------------
  api_projekt/
  |-- app/
  |   |-- __init__.py
  |   |-- main.py
  |   |-- config.py
  |   |-- models/
  |   |   |-- __init__.py
  |   |   |-- user.py
  |   |-- routers/
  |   |   |-- __init__.py
  |   |   |-- users.py
  |   |   |-- items.py
  |   |-- schemas/
  |   |   |-- user.py
  |   |-- services/
  |   |   |-- user_service.py
  |   |-- dependencies.py
  |-- tests/
  |-- requirements.txt
  |-- Dockerfile

VERSIONIERUNG
-------------
  # URL-Prefix:
  app = FastAPI()

  v1_router = APIRouter(prefix="/api/v1")
  v2_router = APIRouter(prefix="/api/v2")

  app.include_router(v1_router)
  app.include_router(v2_router)

RATE LIMITING
-------------
  from slowapi import Limiter, _rate_limit_exceeded_handler
  from slowapi.util import get_remote_address

  limiter = Limiter(key_func=get_remote_address)
  app.state.limiter = limiter

  @app.get("/limited")
  @limiter.limit("5/minute")
  async def limited_endpoint(request: Request):
      return {"status": "ok"}

BACH-INTEGRATION
================
  Partner-Zuweisung:
    - Claude: API-Design, Endpoint-Planung
    - Copilot: Boilerplate-Code generieren
    - Postman/Insomnia: API-Testing

  Typische BACH-APIs:
    - Dokumenten-Verarbeitung
    - LLM-Proxy-Services
    - Automatisierungs-Webhooks

CHECKLISTE FUER PRODUCTION
==========================
  [ ] CORS konfiguriert
  [ ] Authentifizierung implementiert
  [ ] Rate Limiting aktiv
  [ ] Logging eingerichtet
  [ ] Error Handling vollstaendig
  [ ] Tests geschrieben
  [ ] Dokumentation aktuell
  [ ] Environment Variables fuer Secrets
  [ ] Health Check Endpoint (/health)
  [ ] HTTPS aktiviert

SIEHE AUCH
==========
  wiki/python/best_practices/      Python Best Practices
  wiki/python/multithreading/      Async/Await Grundlagen
  wiki/webapps/                    Web-Anwendungen allgemein
  wiki/informatik/devops/          Deployment und CI/CD
