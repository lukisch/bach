# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: React Docs, Vue.js Docs, Angular Docs, MDN Web Docs, State of JS 2025

WEB-FRAMEWORKS UEBERSICHT
=========================

Stand: 2026-02-05

Web-Frameworks sind Softwarebibliotheken, die wiederverwendbare
Loesungen fuer gaengige Webentwicklungs-Aufgaben bereitstellen.
Sie erhoehen die Produktivitaet und foerdern Best Practices.

FRONTEND FRAMEWORKS
===================

  REACT (META)
  ------------
  Deklarative, komponentenbasierte UI-Bibliothek.

  Kernkonzepte:
    - Virtual DOM fuer Performance
    - JSX (JavaScript + HTML)
    - Unidirektionaler Datenfluss
    - Hooks fuer State und Lifecycle

  Beispiel (Functional Component):
    import { useState, useEffect } from 'react';

    function UserList() {
      const [users, setUsers] = useState([]);
      const [loading, setLoading] = useState(true);

      useEffect(() => {
        fetch('/api/users')
          .then(res => res.json())
          .then(data => {
            setUsers(data);
            setLoading(false);
          });
      }, []);

      if (loading) return <p>Laden...</p>;

      return (
        <ul>
          {users.map(user => (
            <li key={user.id}>{user.name}</li>
          ))}
        </ul>
      );
    }

  Wichtige Hooks:
    useState      Lokaler State
    useEffect     Side Effects, Lifecycle
    useContext    Context-API Zugriff
    useReducer    Komplexer State
    useMemo       Memoization
    useCallback   Callback-Memoization
    useRef        Referenzen, DOM-Zugriff

  Oekosystem:
    React Router  Routing
    Redux/Zustand State Management
    React Query   Server State
    Framer Motion Animationen

  VUE.JS
  ------
  Progressives Framework mit reaktivem System.

  Kernkonzepte:
    - Reaktivitaetssystem
    - Single File Components (.vue)
    - Composition API (Vue 3)
    - Two-Way Data Binding

  Beispiel (Composition API):
    <script setup>
    import { ref, onMounted, computed } from 'vue'

    const users = ref([])
    const loading = ref(true)
    const searchTerm = ref('')

    const filteredUsers = computed(() =>
      users.value.filter(u =>
        u.name.toLowerCase().includes(searchTerm.value.toLowerCase())
      )
    )

    onMounted(async () => {
      const res = await fetch('/api/users')
      users.value = await res.json()
      loading.value = false
    })
    </script>

    <template>
      <input v-model="searchTerm" placeholder="Suchen...">
      <p v-if="loading">Laden...</p>
      <ul v-else>
        <li v-for="user in filteredUsers" :key="user.id">
          {{ user.name }}
        </li>
      </ul>
    </template>

  Oekosystem:
    Vue Router    Routing
    Pinia         State Management (Vuex Nachfolger)
    VueUse        Composition Utilities
    Vuetify       UI Komponenten

  ANGULAR (GOOGLE)
  ----------------
  Vollstaendiges, opinionated Framework fuer Enterprise.

  Kernkonzepte:
    - TypeScript als Standard
    - Dependency Injection
    - Modulsystem
    - RxJS fuer Reactive Programming

  Beispiel (Component):
    import { Component, OnInit } from '@angular/core';
    import { HttpClient } from '@angular/common/http';
    import { Observable } from 'rxjs';

    interface User {
      id: number;
      name: string;
    }

    @Component({
      selector: 'app-user-list',
      template: `
        <ul>
          <li *ngFor="let user of users$ | async">
            {{ user.name }}
          </li>
        </ul>
      `
    })
    export class UserListComponent implements OnInit {
      users$: Observable<User[]>;

      constructor(private http: HttpClient) {}

      ngOnInit() {
        this.users$ = this.http.get<User[]>('/api/users');
      }
    }

  Oekosystem:
    Angular Router    Eingebaut
    NgRx              State Management
    Angular Material  UI Komponenten
    Angular CLI       Entwicklungstools

  SVELTE
  ------
  Compiler-basierter Ansatz ohne Runtime-Overhead.

  Kernkonzepte:
    - Kompiliert zu Vanilla JS
    - Reaktivitaet durch Zuweisung
    - Weniger Boilerplate
    - Kleine Bundle-Groesse

  Beispiel:
    <script>
      let users = [];
      let loading = true;
      let searchTerm = '';

      $: filteredUsers = users.filter(u =>
        u.name.toLowerCase().includes(searchTerm.toLowerCase())
      );

      async function loadUsers() {
        const res = await fetch('/api/users');
        users = await res.json();
        loading = false;
      }

      loadUsers();
    </script>

    <input bind:value={searchTerm} placeholder="Suchen...">

    {#if loading}
      <p>Laden...</p>
    {:else}
      <ul>
        {#each filteredUsers as user (user.id)}
          <li>{user.name}</li>
        {/each}
      </ul>
    {/if}

BACKEND FRAMEWORKS
==================

  EXPRESS.JS (NODE.JS)
  --------------------
  Minimales, flexibles Web-Framework.

  Beispiel:
    const express = require('express');
    const app = express();

    app.use(express.json());

    // Middleware
    app.use((req, res, next) => {
      console.log(`${req.method} ${req.path}`);
      next();
    });

    // Routes
    app.get('/api/users', async (req, res) => {
      const users = await User.findAll();
      res.json(users);
    });

    app.post('/api/users', async (req, res) => {
      const user = await User.create(req.body);
      res.status(201).json(user);
    });

    // Error Handling
    app.use((err, req, res, next) => {
      console.error(err);
      res.status(500).json({ error: 'Server Error' });
    });

    app.listen(3000);

  Oekosystem:
    Passport      Authentifizierung
    Helmet        Security Headers
    Morgan        Logging
    Multer        File Upload

  DJANGO (PYTHON)
  ---------------
  Batteries-included Framework mit Admin, ORM, Auth.

  Struktur:
    myproject/
    ├── manage.py
    ├── myproject/
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── myapp/
        ├── models.py
        ├── views.py
        ├── urls.py
        └── templates/

  Model Beispiel:
    from django.db import models

    class User(models.Model):
        name = models.CharField(max_length=100)
        email = models.EmailField(unique=True)
        created_at = models.DateTimeField(auto_now_add=True)

        class Meta:
            ordering = ['-created_at']

  View Beispiel (Class-Based):
    from django.views.generic import ListView
    from rest_framework import viewsets

    class UserListView(ListView):
        model = User
        template_name = 'users/list.html'

    # Django REST Framework
    class UserViewSet(viewsets.ModelViewSet):
        queryset = User.objects.all()
        serializer_class = UserSerializer

  FLASK (PYTHON)
  --------------
  Microframework fuer Python - minimalistisch und flexibel.

  Beispiel:
    from flask import Flask, jsonify, request
    from flask_sqlalchemy import SQLAlchemy

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    db = SQLAlchemy(app)

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))

    @app.route('/api/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        return jsonify([{'id': u.id, 'name': u.name} for u in users])

    @app.route('/api/users', methods=['POST'])
    def create_user():
        data = request.json
        user = User(name=data['name'])
        db.session.add(user)
        db.session.commit()
        return jsonify({'id': user.id}), 201

  FASTAPI (PYTHON)
  ----------------
  Modernes, schnelles Framework mit automatischer Dokumentation.

  Beispiel:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    from typing import List

    app = FastAPI()

    class UserCreate(BaseModel):
        name: str
        email: str

    class User(UserCreate):
        id: int

    @app.get("/api/users", response_model=List[User])
    async def get_users():
        return await User.all()

    @app.post("/api/users", response_model=User, status_code=201)
    async def create_user(user: UserCreate):
        return await User.create(**user.dict())

  Vorteile:
    - Automatische OpenAPI-Dokumentation
    - Type Hints mit Pydantic
    - Async/Await native
    - Sehr hohe Performance

  SPRING BOOT (JAVA)
  ------------------
  Enterprise-Framework mit Dependency Injection.

  Controller Beispiel:
    @RestController
    @RequestMapping("/api/users")
    public class UserController {

        @Autowired
        private UserService userService;

        @GetMapping
        public List<User> getAllUsers() {
            return userService.findAll();
        }

        @PostMapping
        @ResponseStatus(HttpStatus.CREATED)
        public User createUser(@RequestBody @Valid UserDTO dto) {
            return userService.create(dto);
        }

        @GetMapping("/{id}")
        public User getUser(@PathVariable Long id) {
            return userService.findById(id)
                .orElseThrow(() -> new NotFoundException());
        }
    }

  Oekosystem:
    Spring Security   Auth & Authorization
    Spring Data JPA   Database Access
    Spring Cloud      Microservices
    Spring Actuator   Monitoring

FULLSTACK FRAMEWORKS
====================

  NEXT.JS (REACT)
  ---------------
  React-Framework mit Server-Side Rendering.

  Features:
    - File-based Routing (App Router)
    - Server Components
    - API Routes
    - Static Site Generation (SSG)
    - Server-Side Rendering (SSR)
    - Incremental Static Regeneration

  Beispiel (App Router):
    // app/users/page.tsx
    async function getUsers() {
      const res = await fetch('https://api.example.com/users');
      return res.json();
    }

    export default async function UsersPage() {
      const users = await getUsers();

      return (
        <ul>
          {users.map(user => (
            <li key={user.id}>{user.name}</li>
          ))}
        </ul>
      );
    }

    // app/api/users/route.ts
    import { NextResponse } from 'next/server';

    export async function GET() {
      const users = await db.user.findMany();
      return NextResponse.json(users);
    }

  NUXT (VUE)
  ----------
  Vue-Framework mit SSR und Auto-Import.

  Beispiel:
    // pages/users.vue
    <script setup>
    const { data: users } = await useFetch('/api/users')
    </script>

    <template>
      <ul>
        <li v-for="user in users" :key="user.id">
          {{ user.name }}
        </li>
      </ul>
    </template>

    // server/api/users.get.ts
    export default defineEventHandler(async () => {
      return await db.user.findMany()
    })

  REMIX
  -----
  Web Standards-fokussiertes React-Framework.

  Beispiel:
    // app/routes/users.tsx
    import { json, LoaderFunctionArgs } from '@remix-run/node';
    import { useLoaderData } from '@remix-run/react';

    export async function loader({ request }: LoaderFunctionArgs) {
      const users = await db.user.findMany();
      return json({ users });
    }

    export default function Users() {
      const { users } = useLoaderData<typeof loader>();
      return (
        <ul>
          {users.map(user => (
            <li key={user.id}>{user.name}</li>
          ))}
        </ul>
      );
    }

  SVELTEKIT
  ---------
  Fullstack-Framework fuer Svelte.

  Beispiel:
    // src/routes/users/+page.server.ts
    export async function load() {
      const users = await db.user.findMany();
      return { users };
    }

    // src/routes/users/+page.svelte
    <script>
      export let data;
    </script>

    <ul>
      {#each data.users as user}
        <li>{user.name}</li>
      {/each}
    </ul>

CSS FRAMEWORKS
==============

  TAILWIND CSS
  ------------
  Utility-First CSS Framework.

  Beispiel:
    <button class="bg-blue-500 hover:bg-blue-700 text-white
                   font-bold py-2 px-4 rounded shadow-lg
                   transition duration-300 ease-in-out">
      Klick mich
    </button>

  Vorteile:
    - Schnelle Entwicklung
    - Konsistentes Design
    - Kleine Bundle-Groesse (PurgeCSS)
    - Responsive: sm:, md:, lg:

  BOOTSTRAP
  ---------
  Klassisches CSS Framework mit Komponenten.

  Beispiel:
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Titel</h5>
        <p class="card-text">Inhalt</p>
        <a href="#" class="btn btn-primary">Button</a>
      </div>
    </div>

VERGLEICHSTABELLE
=================

  Framework    Typ        Sprache     Lernkurve   Groesse
  ---------------------------------------------------------------
  React        Frontend   JavaScript  Mittel      Klein
  Vue          Frontend   JavaScript  Niedrig     Klein
  Angular      Frontend   TypeScript  Hoch        Gross
  Svelte       Frontend   JavaScript  Niedrig     Minimal

  Express      Backend    JavaScript  Niedrig     Minimal
  Django       Backend    Python      Mittel      Gross
  FastAPI      Backend    Python      Niedrig     Klein
  Spring Boot  Backend    Java        Hoch        Gross

  Next.js      Fullstack  JavaScript  Mittel      Mittel
  Nuxt         Fullstack  JavaScript  Mittel      Mittel

AUSWAHLKRITERIEN
================

  TEAMGROESSE
  -----------
    Kleines Team     Svelte, Vue, Express
    Grosses Team     Angular, Spring Boot
    Solo             Next.js, Nuxt

  PROJEKTART
  ----------
    Startup/MVP      Next.js, FastAPI
    Enterprise       Angular, Spring Boot
    Content Site     Nuxt, Astro
    API              FastAPI, Express

  PERFORMANCE
  -----------
    Kritisch         Svelte, FastAPI, Go
    Standard         React, Django
    SEO-wichtig      Next.js, Nuxt

SIEHE AUCH
==========
  wiki/webapps/frontend/README.txt
  wiki/webapps/backend/README.txt
  wiki/webapps/README.txt
  wiki/python/README.txt
  wiki/java/README.txt
