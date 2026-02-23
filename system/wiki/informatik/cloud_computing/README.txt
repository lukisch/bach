# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: AWS/Azure/GCP Dokumentation, NIST Cloud Computing Definition, Cloud Native Computing Foundation

CLOUD COMPUTING
===============

Stand: 2026-02-05

DEFINITION
==========
Cloud Computing bezeichnet die Bereitstellung von IT-Ressourcen (Rechenleistung,
Speicher, Anwendungen) ueber das Internet. Nutzer zahlen nur fuer tatsaechlich
genutzte Ressourcen (Pay-as-you-go) und koennen bei Bedarf skalieren.


NIST-DEFINITION (5 MERKMALE)
============================
Das National Institute of Standards and Technology definiert Cloud Computing
durch fuenf wesentliche Charakteristiken:

  1. On-Demand Self-Service
  -------------------------
     - Ressourcen ohne menschliche Interaktion mit Anbieter buchbar
     - APIs und Web-Konsolen fuer Selbstverwaltung

  2. Broad Network Access
  -----------------------
     - Zugriff ueber Standard-Netzwerkmechanismen
     - Von verschiedenen Geraeten (Laptop, Smartphone, etc.)

  3. Resource Pooling
  -------------------
     - Ressourcen werden von mehreren Nutzern geteilt (Multi-Tenancy)
     - Physische Standorte abstrakt (der Nutzer weiss nicht, wo)

  4. Rapid Elasticity
  -------------------
     - Ressourcen schnell skalierbar (hoch und runter)
     - Erscheint fuer Nutzer unbegrenzt

  5. Measured Service
  -------------------
     - Nutzung wird gemessen und abgerechnet
     - Transparenz fuer Anbieter und Nutzer


SERVICE-MODELLE
===============

  IaaS (Infrastructure as a Service):
  -----------------------------------
    Was: Virtuelle Maschinen, Netzwerk, Storage
    Kontrolle: Betriebssystem aufwaerts
    Beispiele: AWS EC2, Azure VMs, Google Compute Engine

    Anwendung:
      - Eigene Server ohne physische Hardware
      - Volle Kontrolle ueber Konfiguration
      - Migration von On-Premise zu Cloud

  PaaS (Platform as a Service):
  -----------------------------
    Was: Laufzeitumgebung, Datenbanken, Middleware
    Kontrolle: Anwendungscode, keine Infra-Verwaltung
    Beispiele: Heroku, Google App Engine, Azure App Service

    Anwendung:
      - Schnelle Anwendungsentwicklung
      - Kein Infrastruktur-Management
      - Auto-Scaling inklusive

  SaaS (Software as a Service):
  -----------------------------
    Was: Fertige Anwendungen ueber Browser
    Kontrolle: Nur Nutzung und Konfiguration
    Beispiele: Microsoft 365, Salesforce, Google Workspace

    Anwendung:
      - Sofort nutzbar ohne Installation
      - Automatische Updates
      - Keine Wartung erforderlich

  FaaS (Function as a Service / Serverless):
  ------------------------------------------
    Was: Einzelne Funktionen, event-getrieben
    Kontrolle: Nur Funktionscode
    Beispiele: AWS Lambda, Azure Functions, Google Cloud Functions

    Anwendung:
      - Event-getriebene Workloads
      - Kosten nur bei Ausfuehrung
      - Keine Server-Verwaltung


DEPLOYMENT-MODELLE
==================

  Public Cloud:
  -------------
    - Ressourcen oeffentlich verfuegbar (gegen Bezahlung)
    - Multi-Tenant Infrastruktur
    - Skalierbarkeit und Kosteneffizienz
    - Beispiele: AWS, Azure, GCP

  Private Cloud:
  --------------
    - Dedizierte Infrastruktur fuer eine Organisation
    - Hoehere Kontrolle und Sicherheit
    - On-Premise oder Hosted
    - Beispiele: VMware, OpenStack

  Hybrid Cloud:
  -------------
    - Kombination aus Public und Private
    - Sensitive Daten privat, Burst in Public
    - Komplexere Verwaltung
    - Beispiele: Azure Arc, AWS Outposts

  Multi-Cloud:
  ------------
    - Nutzung mehrerer Cloud-Anbieter
    - Vermeidung von Vendor Lock-in
    - Best-of-Breed Ansatz
    - Erfordert Abstraktionsschicht


DIE GROSSEN DREI ANBIETER
=========================

  AWS (Amazon Web Services):
  --------------------------
    Marktanteil: ~32% (Marktfuehrer)
    Staerken:
      - Breitestes Service-Angebot (200+ Services)
      - Groesstes globales Netzwerk
      - Ausgereiftes Oekosystem

    Wichtige Services:
      EC2           - Virtuelle Maschinen
      S3            - Object Storage
      Lambda        - Serverless Functions
      RDS           - Managed Databases
      EKS           - Managed Kubernetes
      CloudFront    - CDN

  Azure (Microsoft):
  ------------------
    Marktanteil: ~23%
    Staerken:
      - Enterprise-Integration (Active Directory)
      - Hybrid Cloud (Azure Arc)
      - Microsoft-Oekosystem (Office 365, Teams)

    Wichtige Services:
      Virtual Machines  - VMs
      Blob Storage      - Object Storage
      Azure Functions   - Serverless
      Azure SQL         - Managed Database
      AKS               - Managed Kubernetes

  GCP (Google Cloud Platform):
  ----------------------------
    Marktanteil: ~10%
    Staerken:
      - Kubernetes (entwickelt von Google)
      - ML/AI Services (TensorFlow, Vertex AI)
      - BigQuery (Data Warehouse)

    Wichtige Services:
      Compute Engine    - VMs
      Cloud Storage     - Object Storage
      Cloud Functions   - Serverless
      Cloud SQL         - Managed Database
      GKE               - Managed Kubernetes


CORE SERVICES IM DETAIL
=======================

  Compute:
  --------
    # AWS EC2 Instanz starten (CLI)
    aws ec2 run-instances \
      --image-id ami-0123456789abcdef0 \
      --instance-type t3.micro \
      --key-name my-key \
      --security-group-ids sg-12345678

    Instanz-Typen (AWS Beispiel):
      t3.micro      - Burst, guenstig, Development
      m6i.large     - General Purpose, Production
      c6i.xlarge    - Compute-optimiert
      r6i.large     - Memory-optimiert
      p4d.24xlarge  - GPU fuer ML

  Storage:
  --------
    Object Storage (S3, Blob, GCS):
      - Unstrukturierte Daten (Bilder, Videos, Backups)
      - Unbegrenzte Skalierung
      - 11x9 Durability (99.999999999%)

    Block Storage (EBS, Azure Disk):
      - Fuer VM-Festplatten
      - Persistente Speicherung

    File Storage (EFS, Azure Files):
      - Geteilter Dateizugriff (NFS/SMB)
      - Fuer Legacy-Anwendungen

    # S3 Bucket erstellen und Datei hochladen
    aws s3 mb s3://mein-bucket
    aws s3 cp datei.txt s3://mein-bucket/

  Databases:
  ----------
    Relational (RDS, Cloud SQL):
      - MySQL, PostgreSQL, SQL Server
      - Managed: Backups, Patches, HA

    NoSQL (DynamoDB, CosmosDB):
      - Key-Value, Document, Graph
      - Horizontal skalierbar

    Data Warehouse (Redshift, BigQuery):
      - Analytische Abfragen
      - Petabyte-Skala


NETZWERK UND SICHERHEIT
=======================

  Virtual Private Cloud (VPC):
  ----------------------------
    - Isoliertes virtuelles Netzwerk
    - Subnets, Route Tables, Gateways
    - Network ACLs und Security Groups

    VPC-Architektur Beispiel:
      VPC (10.0.0.0/16)
        |-- Public Subnet (10.0.1.0/24)   -> Internet Gateway
        |-- Private Subnet (10.0.2.0/24)  -> NAT Gateway
        |-- Database Subnet (10.0.3.0/24) -> Kein Internet

  Load Balancing:
  ---------------
    Application Load Balancer (ALB)  - Layer 7, HTTP/HTTPS
    Network Load Balancer (NLB)      - Layer 4, TCP/UDP
    Global Load Balancer             - Multi-Region

  CDN (Content Delivery Network):
  -------------------------------
    CloudFront (AWS), Azure CDN, Cloud CDN
    - Statische Inhalte am Edge cachen
    - Niedrigere Latenz fuer Endnutzer
    - DDoS-Schutz

  Identity & Access Management (IAM):
  -----------------------------------
    Prinzipien:
      - Least Privilege (minimale Rechte)
      - Role-Based Access Control (RBAC)
      - MFA fuer alle Accounts

    # AWS IAM Policy Beispiel
    {
      "Version": "2012-10-17",
      "Statement": [{
        "Effect": "Allow",
        "Action": ["s3:GetObject", "s3:PutObject"],
        "Resource": "arn:aws:s3:::mein-bucket/*"
      }]
    }


KOSTENMANAGEMENT
================

  Preismodelle:
  -------------
    On-Demand         - Volle Flexibilitaet, hoechster Preis
    Reserved          - 1-3 Jahre Commitment, bis 75% Rabatt
    Spot/Preemptible  - Ueberschusskapazitaet, bis 90% Rabatt
    Savings Plans     - Flexibler als Reserved, guter Rabatt

  Kostenoptimierung:
  ------------------
    1. Right-Sizing   - Passende Instanz-Groesse waehlen
    2. Auto-Scaling   - Ressourcen nach Bedarf
    3. Reserved       - Fuer stabile Workloads
    4. Spot           - Fuer unterbrechbare Workloads
    5. Tagging        - Kosten nach Teams/Projekten
    6. Cleanup        - Ungenutzte Ressourcen loeschen

  Tools:
  ------
    AWS Cost Explorer       - Kostenanalyse
    Azure Cost Management   - Budgets und Alerts
    Infracost               - Terraform Kosten-Schaetzung


SERVERLESS ARCHITEKTUR
======================
Code ausfuehren ohne Server zu verwalten.

  AWS Lambda Beispiel:
  --------------------
    # lambda_function.py
    import json

    def handler(event, context):
        name = event.get('name', 'World')
        return {
            'statusCode': 200,
            'body': json.dumps(f'Hello, {name}!')
        }

  Serverless Framework Deployment:
  --------------------------------
    # serverless.yml
    service: hello-service
    provider:
      name: aws
      runtime: python3.12
      region: eu-central-1

    functions:
      hello:
        handler: handler.handler
        events:
          - http:
              path: hello
              method: get

  Typische Serverless Architektur:
  --------------------------------
    API Gateway -> Lambda -> DynamoDB
         |
         +-> S3 (Static Files)
         +-> Cognito (Auth)


BEST PRACTICES
==============

  Architektur:
  ------------
    - Design for Failure (alles kann ausfallen)
    - Stateless Services (Zustand in Datenbank/Cache)
    - Microservices statt Monolith (wo sinnvoll)
    - Infrastructure as Code (Terraform, CloudFormation)

  Sicherheit:
  -----------
    - Keine Credentials im Code (Secrets Manager, SSM)
    - VPC fuer alle Ressourcen
    - Verschluesselung at Rest und in Transit
    - WAF fuer Web-Anwendungen
    - Regular Security Audits

  Zuverlaessigkeit:
  -----------------
    - Multi-AZ Deployments (Hochverfuegbarkeit)
    - Backups automatisieren
    - Disaster Recovery Plan
    - Chaos Engineering (Ausfaelle simulieren)

  Performance:
  ------------
    - Caching (ElastiCache, CloudFront)
    - Read Replicas fuer Datenbanken
    - Asynchrone Verarbeitung (SQS, SNS)
    - Monitoring und Alerting


CLOUD-NATIVE ENTWICKLUNG
========================

  12-Factor App Prinzipien:
  -------------------------
    1. Codebase       - Ein Repo pro App
    2. Dependencies   - Explizit deklarieren
    3. Config         - Umgebungsvariablen
    4. Backing Svcs   - Als Ressourcen behandeln
    5. Build/Release  - Strikt trennen
    6. Processes      - Stateless
    7. Port Binding   - Services exportieren Ports
    8. Concurrency    - Horizontal skalieren
    9. Disposability  - Schneller Start/Stop
   10. Dev/Prod Parity - Umgebungen angleichen
   11. Logs           - Als Event Streams
   12. Admin          - One-off Prozesse


SIEHE AUCH
==========
  wiki/informatik/devops/             DevOps und CI/CD
  wiki/informatik/netzwerke/          Netzwerk-Grundlagen
  wiki/informatik/software_architektur/  Microservices
  wiki/webapps/deployment/            Web-Deployment
