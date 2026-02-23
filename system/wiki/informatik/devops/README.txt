# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: The DevOps Handbook (Kim et al.), Google SRE Book, Docker/Kubernetes Dokumentation

DEVOPS
======

Stand: 2026-02-05

DEFINITION
==========
DevOps ist eine Kultur und Methodik, die Softwareentwicklung (Dev) und
IT-Betrieb (Ops) vereint. Ziel ist die Beschleunigung des Software-
Lebenszyklus durch Automatisierung, Zusammenarbeit und kontinuierliches
Feedback.


KERNPRINZIPIEN
==============

  Die Drei Wege (The Three Ways):
  -------------------------------
    1. Flow          - Schneller Fluss von Dev zu Ops zu Kunde
    2. Feedback      - Schnelle Rueckmeldung auf allen Ebenen
    3. Lernen        - Kontinuierliches Experimentieren und Verbessern

  CALMS-Framework:
  ----------------
    Culture         - Zusammenarbeit und gemeinsame Verantwortung
    Automation      - Wiederholbare Prozesse automatisieren
    Lean            - Verschwendung eliminieren, Wertfluss optimieren
    Measurement     - Alles messen, datengetriebene Entscheidungen
    Sharing         - Wissen und Verantwortung teilen


CONTINUOUS INTEGRATION (CI)
===========================
Automatische Integration von Code-Aenderungen.

  Prinzipien:
  -----------
    - Haeufiges Committen (mehrmals taeglich)
    - Automatische Builds bei jedem Commit
    - Automatische Tests (Unit, Integration)
    - Schnelles Feedback bei Fehlern
    - Trunk-Based Development bevorzugt

  CI-Pipeline Beispiel (GitHub Actions):
  --------------------------------------
    # .github/workflows/ci.yml
    name: CI Pipeline
    on: [push, pull_request]

    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - name: Setup Python
            uses: actions/setup-python@v5
            with:
              python-version: '3.12'
          - name: Install dependencies
            run: pip install -r requirements.txt
          - name: Run tests
            run: pytest tests/ --cov=src
          - name: Lint
            run: flake8 src/

  Beliebte CI-Tools:
  ------------------
    GitHub Actions    - Integriert in GitHub, YAML-basiert
    GitLab CI         - Integriert in GitLab, maechtiges Feature-Set
    Jenkins           - Open Source, sehr flexibel, Plugin-basiert
    CircleCI          - Cloud-basiert, schnell
    Travis CI         - Einfach fuer Open-Source-Projekte


CONTINUOUS DELIVERY/DEPLOYMENT (CD)
===================================
Automatische Bereitstellung von Software.

  Continuous Delivery:
  --------------------
    - Jeder Build ist potenziell produktionsreif
    - Deployment erfordert manuelle Freigabe
    - Reduziert Risiko durch kleine, haeufige Releases

  Continuous Deployment:
  ----------------------
    - Vollautomatisches Deployment ohne manuelle Freigabe
    - Erfordert umfassende Testabdeckung
    - Schnellstes Time-to-Market

  Deployment-Strategien:
  ----------------------
    Blue-Green        - Zwei identische Umgebungen, Umschalten
    Canary            - Schrittweises Rollout (1%, 10%, 50%, 100%)
    Rolling           - Schrittweises Ersetzen von Instanzen
    Feature Flags     - Features zur Laufzeit aktivieren/deaktivieren


CONTAINERISIERUNG MIT DOCKER
============================
Lightweight Virtualisierung fuer portable Anwendungen.

  Grundkonzepte:
  --------------
    Image             - Unveraenderliche Vorlage (Read-only)
    Container         - Laufende Instanz eines Images
    Dockerfile        - Build-Anleitung fuer Images
    Registry          - Speicher fuer Images (Docker Hub, ECR, GCR)

  Dockerfile Beispiel:
  --------------------
    FROM python:3.12-slim
    WORKDIR /app

    # Dependencies zuerst (Cache-Optimierung)
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    # Dann den Code
    COPY src/ ./src/

    # Non-root User fuer Sicherheit
    RUN useradd -m appuser
    USER appuser

    EXPOSE 8000
    CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0"]

  Wichtige Docker-Befehle:
  ------------------------
    docker build -t myapp:1.0 .           # Image bauen
    docker run -d -p 8000:8000 myapp:1.0  # Container starten
    docker ps                              # Laufende Container
    docker logs <container>                # Logs anzeigen
    docker exec -it <container> bash       # Shell im Container

  Docker Compose (Multi-Container):
  ---------------------------------
    # docker-compose.yml
    version: '3.8'
    services:
      web:
        build: .
        ports:
          - "8000:8000"
        environment:
          - DATABASE_URL=postgresql://db:5432/app
        depends_on:
          - db
      db:
        image: postgres:15
        volumes:
          - pgdata:/var/lib/postgresql/data
        environment:
          - POSTGRES_DB=app
          - POSTGRES_PASSWORD=${DB_PASSWORD}

    volumes:
      pgdata:


CONTAINER-ORCHESTRIERUNG MIT KUBERNETES
=======================================
Verwaltung von Container-Clustern im grossen Massstab.

  Kernkomponenten:
  ----------------
    Pod               - Kleinste deploybare Einheit (1+ Container)
    Deployment        - Deklarative Pod-Verwaltung
    Service           - Stabiler Netzwerk-Endpoint fuer Pods
    Ingress           - HTTP/HTTPS Routing von aussen
    ConfigMap/Secret  - Konfiguration und Geheimnisse
    Namespace         - Logische Trennung von Ressourcen

  Deployment Beispiel:
  --------------------
    # deployment.yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: myapp
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: myapp
      template:
        metadata:
          labels:
            app: myapp
        spec:
          containers:
          - name: myapp
            image: myapp:1.0
            ports:
            - containerPort: 8000
            resources:
              requests:
                memory: "128Mi"
                cpu: "100m"
              limits:
                memory: "256Mi"
                cpu: "500m"
            livenessProbe:
              httpGet:
                path: /health
                port: 8000

  Wichtige kubectl-Befehle:
  -------------------------
    kubectl apply -f deployment.yaml      # Ressourcen anwenden
    kubectl get pods                       # Pods anzeigen
    kubectl describe pod <name>            # Pod-Details
    kubectl logs <pod>                     # Pod-Logs
    kubectl exec -it <pod> -- bash         # Shell im Pod
    kubectl rollout restart deployment/x   # Neustart

  Managed Kubernetes:
  -------------------
    EKS (Amazon)      - AWS Integration
    AKS (Azure)       - Azure Integration
    GKE (Google)      - Kubernetes-Erfinder, sehr ausgereift


INFRASTRUCTURE AS CODE (IaC)
============================
Infrastruktur als versionierten Code verwalten.

  Terraform Beispiel:
  -------------------
    # main.tf
    provider "aws" {
      region = "eu-central-1"
    }

    resource "aws_instance" "web" {
      ami           = "ami-0123456789abcdef0"
      instance_type = "t3.micro"

      tags = {
        Name        = "web-server"
        Environment = "production"
      }
    }

    resource "aws_security_group" "web" {
      name = "web-sg"

      ingress {
        from_port   = 443
        to_port     = 443
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
      }
    }

  Terraform-Workflow:
  -------------------
    terraform init      # Provider initialisieren
    terraform plan      # Aenderungen pruefen
    terraform apply     # Aenderungen anwenden
    terraform destroy   # Infrastruktur loeschen

  IaC-Tools im Vergleich:
  -----------------------
    Terraform         - Multi-Cloud, deklarativ, HCL-Syntax
    Ansible           - Agentless, YAML, auch Konfigurationsmanagement
    Pulumi            - IaC in echten Programmiersprachen
    CloudFormation    - AWS-spezifisch, YAML/JSON


MONITORING UND OBSERVABILITY
============================
Einblick in Systeme zur Fehlererkennung und Optimierung.

  Die Drei Saeulen:
  -----------------
    Metrics           - Zahlen ueber Zeit (CPU, RAM, Latenz)
    Logs              - Ereignis-basierte Nachrichten
    Traces            - Anfrage-Pfade durch verteilte Systeme

  Prometheus + Grafana (Metrics):
  -------------------------------
    # prometheus.yml
    scrape_configs:
      - job_name: 'myapp'
        static_configs:
          - targets: ['myapp:8000']

    # Metriken im Code (Python)
    from prometheus_client import Counter, Histogram

    request_count = Counter('http_requests_total', 'Total requests')
    request_latency = Histogram('http_request_duration_seconds', 'Latency')

  ELK-Stack (Logs):
  -----------------
    Elasticsearch     - Speicherung und Suche
    Logstash          - Log-Verarbeitung und -Transformation
    Kibana            - Visualisierung und Dashboards

  Alerting Best Practices:
  ------------------------
    - Nur auf actionable Alerts reagieren
    - Runbooks fuer jeden Alert
    - Eskalationspfade definieren
    - Alert-Fatigue vermeiden (keine Noise-Alerts)


BEST PRACTICES
==============

  Kultur:
  -------
    - Blame-free Post-Mortems nach Incidents
    - Gemeinsame Verantwortung fuer Produktion
    - Dokumentation als Code behandeln
    - Wissensaustausch foerdern (Tech Talks, Pair Programming)

  Sicherheit (DevSecOps):
  -----------------------
    - Security-Scans in CI-Pipeline integrieren
    - Dependency-Scanning (Snyk, Dependabot)
    - Container-Image-Scanning
    - Secrets nie im Code (Vault, AWS Secrets Manager)
    - Least Privilege Prinzip

  Performance:
  ------------
    - Build-Zeiten optimieren (Caching, Parallelisierung)
    - Kleine, inkrementelle Deployments
    - Feature Flags fuer grosse Aenderungen
    - Rollback-Strategie immer bereit haben


METRIKEN (DORA)
===============
DevOps Research and Assessment Metriken.

  Deployment Frequency:
  ---------------------
    Elite:   Mehrmals taeglich
    High:    Woechentlich bis taeglich
    Medium:  Monatlich bis woechentlich
    Low:     Seltener als monatlich

  Lead Time for Changes:
  ----------------------
    Elite:   < 1 Stunde
    High:    1 Tag - 1 Woche
    Medium:  1 Woche - 1 Monat
    Low:     > 1 Monat

  Change Failure Rate:
  --------------------
    Elite:   0-15%
    High:    16-30%
    Medium:  31-45%
    Low:     > 45%

  Time to Restore Service:
  ------------------------
    Elite:   < 1 Stunde
    High:    < 1 Tag
    Medium:  < 1 Woche
    Low:     > 1 Woche


SIEHE AUCH
==========
  wiki/informatik/cloud_computing/       Cloud-Plattformen
  wiki/informatik/software_architektur/  Microservices
  wiki/github_konventionen.txt           Git-Workflows
  wiki/github_einfuehrung.txt            Git-Grundlagen
