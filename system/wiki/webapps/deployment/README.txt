# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: Docker Docs, Kubernetes Docs, AWS/Azure/GCP Dokumentation, CNCF

WEB-APP DEPLOYMENT
==================

Stand: 2026-02-05

Deployment bezeichnet den Prozess, eine Webanwendung von der
Entwicklungsumgebung in eine Produktionsumgebung zu bringen und
dort verfuegbar zu machen. Dieser Artikel behandelt moderne
Deployment-Strategien, Container-Technologien und CI/CD-Pipelines.

HOSTING-OPTIONEN
================

  TRADITIONELLES HOSTING
  ----------------------
  VPS (Virtual Private Server):
    - Eigener virtualisierter Server
    - Volle Kontrolle ueber System
    - Manuelle Wartung noetig
    - Anbieter: Hetzner, DigitalOcean, Linode

  Dedicated Server:
    - Physischer Server nur fuer dich
    - Maximale Performance
    - Teuer, fuer High-Traffic

  Shared Hosting:
    - Mehrere Websites teilen Server
    - Guenstig, eingeschraenkt
    - Fuer kleine Projekte

  CLOUD HOSTING
  -------------
  AWS (Amazon Web Services):
    EC2       Virtual Machines
    S3        Object Storage
    RDS       Managed Databases
    Lambda    Serverless Functions
    ECS/EKS   Container Services

  Azure (Microsoft):
    Virtual Machines
    App Service       Managed Web Apps
    Azure Functions   Serverless
    AKS              Kubernetes Service

  GCP (Google Cloud Platform):
    Compute Engine
    App Engine
    Cloud Run         Serverless Container
    GKE               Kubernetes

  PLATFORM AS A SERVICE (PaaS)
  ----------------------------
  Vorteile:
    - Keine Infrastruktur-Verwaltung
    - Schnelles Deployment
    - Automatisches Scaling
    - Eingebettetes SSL

  Frontend-Plattformen:
    Vercel      Next.js, React (empfohlen fuer Next.js)
    Netlify     JAMstack, Static Sites
    Cloudflare Pages   Edge Deployment

  Backend/Fullstack-Plattformen:
    Heroku      Klassiker, einfach
    Railway     Modern, guenstig
    Render      Docker-basiert
    Fly.io      Edge Computing

CONTAINER-TECHNOLOGIE
=====================

  DOCKER GRUNDLAGEN
  -----------------
  Container virtualisieren auf Betriebssystem-Ebene.
  Vorteile:
    - Konsistente Umgebungen
    - Leichtgewichtig
    - Portabel
    - Isolation

  Dockerfile Beispiel (Node.js):
    # Basis-Image
    FROM node:20-alpine

    # Arbeitsverzeichnis
    WORKDIR /app

    # Dependencies installieren
    COPY package*.json ./
    RUN npm ci --only=production

    # Quellcode kopieren
    COPY . .

    # Port freigeben
    EXPOSE 3000

    # Startbefehl
    CMD ["node", "server.js"]

  Dockerfile Beispiel (Python):
    FROM python:3.12-slim

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    EXPOSE 8000

    CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000"]

  DOCKER BEFEHLE
  --------------
    docker build -t myapp .           Image bauen
    docker run -p 3000:3000 myapp     Container starten
    docker ps                         Laufende Container
    docker logs <container>           Logs anzeigen
    docker stop <container>           Container stoppen
    docker push myregistry/myapp      Image hochladen

  DOCKER COMPOSE
  --------------
  Fuer Multi-Container-Anwendungen:

    # docker-compose.yml
    version: '3.8'

    services:
      web:
        build: .
        ports:
          - "3000:3000"
        environment:
          - DATABASE_URL=postgres://db:5432/app
        depends_on:
          - db

      db:
        image: postgres:15
        volumes:
          - pgdata:/var/lib/postgresql/data
        environment:
          - POSTGRES_DB=app
          - POSTGRES_PASSWORD=secret

    volumes:
      pgdata:

  Befehle:
    docker-compose up -d              Alle Services starten
    docker-compose down               Alle stoppen
    docker-compose logs -f            Logs verfolgen

CONTAINER-ORCHESTRIERUNG
========================

  KUBERNETES (K8s)
  ----------------
  Open-Source Orchestrierungsplattform fuer Container.

  Kernkonzepte:
    Pod           Kleinste Einheit (1+ Container)
    Deployment    Deklarative Updates fuer Pods
    Service       Netzwerk-Abstraktion
    Ingress       HTTP-Routing
    ConfigMap     Konfigurationsdaten
    Secret        Sensible Daten

  Deployment Beispiel:
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: web-app
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: web
      template:
        metadata:
          labels:
            app: web
        spec:
          containers:
          - name: web
            image: myapp:latest
            ports:
            - containerPort: 3000
            resources:
              limits:
                cpu: "500m"
                memory: "256Mi"

  Service Beispiel:
    apiVersion: v1
    kind: Service
    metadata:
      name: web-service
    spec:
      selector:
        app: web
      ports:
        - port: 80
          targetPort: 3000
      type: LoadBalancer

  MANAGED KUBERNETES
  ------------------
    EKS    AWS Elastic Kubernetes Service
    AKS    Azure Kubernetes Service
    GKE    Google Kubernetes Engine

  Vorteile von Managed K8s:
    - Kein Cluster-Management
    - Automatische Updates
    - Integration mit Cloud-Services

CI/CD PIPELINES
===============

  KONZEPT
  -------
  CI = Continuous Integration
    - Automatische Builds bei jedem Commit
    - Automatische Tests
    - Fruehe Fehlererkennung

  CD = Continuous Deployment/Delivery
    - Automatisches Deployment nach erfolgreichen Tests
    - Schnelle Releases
    - Weniger manuelle Arbeit

  GITHUB ACTIONS
  --------------
  Beispiel-Workflow (.github/workflows/deploy.yml):

    name: Deploy

    on:
      push:
        branches: [main]

    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-node@v4
            with:
              node-version: '20'
          - run: npm ci
          - run: npm test

      build:
        needs: test
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - uses: docker/setup-buildx-action@v3
          - uses: docker/login-action@v3
            with:
              registry: ghcr.io
              username: ${{ github.actor }}
              password: ${{ secrets.GITHUB_TOKEN }}
          - uses: docker/build-push-action@v5
            with:
              push: true
              tags: ghcr.io/${{ github.repository }}:latest

      deploy:
        needs: build
        runs-on: ubuntu-latest
        steps:
          - name: Deploy to Server
            uses: appleboy/ssh-action@v1
            with:
              host: ${{ secrets.HOST }}
              username: ${{ secrets.USER }}
              key: ${{ secrets.SSH_KEY }}
              script: |
                docker pull ghcr.io/${{ github.repository }}:latest
                docker-compose up -d

  GITLAB CI
  ---------
  Beispiel (.gitlab-ci.yml):

    stages:
      - test
      - build
      - deploy

    test:
      stage: test
      image: node:20
      script:
        - npm ci
        - npm test

    build:
      stage: build
      image: docker:latest
      services:
        - docker:dind
      script:
        - docker build -t $CI_REGISTRY_IMAGE .
        - docker push $CI_REGISTRY_IMAGE

    deploy:
      stage: deploy
      script:
        - ssh user@server "docker pull && docker-compose up -d"
      only:
        - main

DEPLOYMENT-STRATEGIEN
=====================

  BLUE-GREEN DEPLOYMENT
  ---------------------
  Zwei identische Produktionsumgebungen:
    - Blue: Aktuelle Version
    - Green: Neue Version

  Ablauf:
    1. Green mit neuer Version deployen
    2. Testen auf Green
    3. Traffic von Blue zu Green umleiten
    4. Blue wird zum naechsten Green

  Vorteile:
    - Kein Downtime
    - Schnelles Rollback

  CANARY RELEASES
  ---------------
  Schrittweises Rollout an Subset der Nutzer:

    1. 5% der Nutzer bekommen neue Version
    2. Monitoring und Metriken pruefen
    3. Bei Erfolg: Rollout erhoehen (25%, 50%, 100%)
    4. Bei Problemen: Sofortiges Rollback

  ROLLING UPDATES
  ---------------
  Pods werden schrittweise ersetzt:
    - Keine Downtime
    - Kubernetes-Standard
    - Kann bei Problemen pausieren

  Kubernetes Rolling Update Config:
    spec:
      strategy:
        type: RollingUpdate
        rollingUpdate:
          maxSurge: 1
          maxUnavailable: 0

  FEATURE FLAGS
  -------------
  Neue Features hinter Flags verstecken:

    if (featureFlags.isEnabled('new-checkout')) {
      showNewCheckout();
    } else {
      showOldCheckout();
    }

  Tools: LaunchDarkly, Unleash, Flagsmith

SSL/TLS KONFIGURATION
=====================

  LET'S ENCRYPT
  -------------
  Kostenlose SSL-Zertifikate mit automatischer Erneuerung.

  Mit Certbot (Nginx):
    sudo certbot --nginx -d example.com -d www.example.com

  Automatische Erneuerung:
    sudo certbot renew --dry-run

  MIT TRAEFIK (DOCKER)
  --------------------
  Automatisches SSL fuer Container:

    # traefik.yml
    certificatesResolvers:
      letsencrypt:
        acme:
          email: admin@example.com
          storage: /acme.json
          httpChallenge:
            entryPoint: web

  CDN-INTEGRATION
  ---------------
  Cloudflare, AWS CloudFront, etc.:
    - SSL-Terminierung am Edge
    - Einfache Konfiguration
    - DDoS-Schutz inklusive

MONITORING & OBSERVABILITY
==========================

  LOGGING
  -------
    - Structured Logging (JSON)
    - Zentrales Log-Management
    - Tools: ELK Stack, Loki, CloudWatch

  METRIKEN
  --------
    - Response Times
    - Error Rates
    - CPU/Memory Usage
    - Tools: Prometheus, Grafana, Datadog

  ALERTING
  --------
    - Automatische Benachrichtigungen
    - Eskalationsketten
    - Tools: PagerDuty, Opsgenie

BEST PRACTICES
==============

  SICHERHEIT
  ----------
    - Secrets nie im Code
    - Environment Variables nutzen
    - Regelmässige Updates
    - Security Scans in Pipeline

  PERFORMANCE
  -----------
    - CDN fuer statische Assets
    - Gzip/Brotli Kompression
    - Image Optimization
    - Caching-Strategien

  ZUVERLAESSIGKEIT
  ----------------
    - Health Checks implementieren
    - Graceful Shutdown
    - Retry-Logic
    - Circuit Breaker Pattern

  KOSTEN
  ------
    - Auto-Scaling mit Limits
    - Spot/Preemptible Instances
    - Ressourcen-Monitoring
    - Unused Resources entfernen

CHECKLISTE VOR DEPLOYMENT
=========================

  [ ] Tests erfolgreich
  [ ] Build kompiliert
  [ ] Environment Variables gesetzt
  [ ] SSL-Zertifikat konfiguriert
  [ ] Health Checks funktionieren
  [ ] Rollback-Plan vorhanden
  [ ] Monitoring eingerichtet
  [ ] Logs erreichbar
  [ ] Backup vorhanden
  [ ] Team informiert

SIEHE AUCH
==========
  wiki/informatik/devops/README.txt
  wiki/informatik/cloud_computing/README.txt
  wiki/webapps/README.txt
  wiki/github_konventionen.txt
