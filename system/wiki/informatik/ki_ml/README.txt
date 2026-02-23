# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: Deep Learning Book (Goodfellow), PyTorch Docs, TensorFlow Docs, Papers with Code

KUENSTLICHE INTELLIGENZ UND MACHINE LEARNING
=============================================

Stand: 2026-02-05

Kuenstliche Intelligenz (KI) bezeichnet Systeme, die menschenaehnliche
Intelligenzleistungen erbringen. Machine Learning (ML) ist ein Teilgebiet
der KI, bei dem Algorithmen aus Daten lernen, anstatt explizit
programmiert zu werden.

GRUNDLAGEN
==========

  BEGRIFFSHIERARCHIE
  ------------------
    Kuenstliche Intelligenz (KI/AI)
    └── Machine Learning (ML)
        └── Deep Learning (DL)
            └── Large Language Models (LLMs)

  KUENSTLICHE INTELLIGENZ
  -----------------------
  Definition: Maschinen, die Aufgaben ausfuehren, die
  typischerweise menschliche Intelligenz erfordern.

  Typen:
    Schwache KI (Narrow AI)   Spezialisiert auf eine Aufgabe
                              Beispiele: Schach, Bilderkennung
                              Aktueller Stand der Technik

    Starke KI (AGI)           Allgemeine menschliche Intelligenz
                              Theoretisches Konzept
                              Noch nicht erreicht

    Superintelligenz          Uebertrifft menschliche Intelligenz
                              Spekulativ

  MACHINE LEARNING
  ----------------
  Definition: Algorithmen, die aus Daten lernen und sich
  verbessern, ohne explizit programmiert zu werden.

  Grundprinzip:
    1. Daten sammeln
    2. Modell waehlen
    3. Training (Lernen aus Daten)
    4. Evaluation (Testen)
    5. Deployment (Einsatz)

ML-LERNPARADIGMEN
=================

  SUPERVISED LEARNING (UEBERWACHTES LERNEN)
  -----------------------------------------
  Lernen aus gelabelten Daten (Input -> Output).

  Klassifikation:
    - Zuordnung zu diskreten Kategorien
    - Beispiele: Spam-Erkennung, Bilderkennung
    - Metriken: Accuracy, Precision, Recall, F1

  Regression:
    - Vorhersage kontinuierlicher Werte
    - Beispiele: Preisvorhersage, Zeitreihen
    - Metriken: MSE, RMSE, MAE, R²

  Algorithmen:
    - Linear Regression
    - Logistic Regression
    - Decision Trees
    - Random Forest
    - Support Vector Machines (SVM)
    - k-Nearest Neighbors (k-NN)
    - Neuronale Netze

  UNSUPERVISED LEARNING (UNUEBERWACHTES LERNEN)
  ---------------------------------------------
  Lernen aus ungelabelten Daten - Strukturen entdecken.

  Clustering:
    - Gruppierung aehnlicher Datenpunkte
    - Beispiele: Kundensegmentierung
    - Algorithmen: k-Means, DBSCAN, Hierarchisch

  Dimensionsreduktion:
    - Reduktion der Feature-Anzahl
    - Beispiele: Visualisierung, Preprocessing
    - Algorithmen: PCA, t-SNE, UMAP

  Anomalieerkennung:
    - Erkennung von Ausreissern
    - Beispiele: Betrugerkennung
    - Algorithmen: Isolation Forest, One-Class SVM

  REINFORCEMENT LEARNING (VERSTAERKENDES LERNEN)
  ----------------------------------------------
  Lernen durch Interaktion mit Umgebung und Belohnung.

  Komponenten:
    Agent         Entscheidungstraeger
    Environment   Umgebung
    State         Aktueller Zustand
    Action        Moegliche Handlungen
    Reward        Belohnung/Strafe
    Policy        Entscheidungsstrategie

  Algorithmen:
    - Q-Learning
    - Deep Q-Network (DQN)
    - Policy Gradient
    - Actor-Critic (A3C, PPO)

  Anwendungen:
    - Spiele (AlphaGo, OpenAI Five)
    - Robotik
    - Autonomes Fahren
    - Empfehlungssysteme

NEURONALE NETZE
===============

  GRUNDKONZEPT
  ------------
  Inspiriert von biologischen Neuronen.

  Aufbau:
    Input Layer  →  Hidden Layers  →  Output Layer
         ↓              ↓                 ↓
    Eingabedaten    Verarbeitung      Ergebnis

  Komponenten:
    Neuron           Verarbeitungseinheit
    Gewichte (w)     Lernbare Parameter
    Bias (b)         Verschiebung
    Aktivierung (f)  Nichtlinearitaet

  Berechnung:
    output = f(sum(inputs * weights) + bias)

  AKTIVIERUNGSFUNKTIONEN
  ----------------------
    ReLU        f(x) = max(0, x)         Standard fuer Hidden Layers
    Sigmoid     f(x) = 1/(1+e^-x)        Output fuer Binaerklassifikation
    Tanh        f(x) = (e^x-e^-x)/(e^x+e^-x)   Werte zwischen -1 und 1
    Softmax     f(x_i) = e^x_i/sum(e^x)  Output fuer Multiklassen

  TRAINING
  --------
  Backpropagation-Algorithmus:
    1. Forward Pass: Berechne Vorhersage
    2. Loss berechnen: Vergleich mit Ground Truth
    3. Backward Pass: Gradientenberechnung
    4. Update: Gewichte anpassen

  Optimizer:
    SGD              Stochastic Gradient Descent
    Adam             Adaptive Moment Estimation (Standard)
    AdamW            Adam mit Weight Decay
    RMSprop          Root Mean Square Propagation

  Hyperparameter:
    Learning Rate    Schrittgroesse beim Lernen
    Batch Size       Anzahl Samples pro Update
    Epochs           Durchlaeufe durch Datensatz
    Regularization   L1, L2, Dropout

DEEP LEARNING ARCHITEKTUREN
===========================

  CONVOLUTIONAL NEURAL NETWORKS (CNN)
  -----------------------------------
  Spezialisiert auf Bilddaten.

  Schichten:
    Convolutional    Feature-Extraktion (Filter)
    Pooling          Dimensionsreduktion
    Fully Connected  Klassifikation

  Beispielarchitektur:
    Input (224x224x3)
    → Conv2D (64 Filter, 3x3)
    → ReLU
    → MaxPool (2x2)
    → Conv2D (128 Filter, 3x3)
    → ReLU
    → MaxPool (2x2)
    → Flatten
    → Dense (512)
    → Dense (num_classes)
    → Softmax

  Bekannte Modelle:
    LeNet       Klassiker fuer Ziffern
    AlexNet     ImageNet Durchbruch 2012
    VGG         Tiefe Netze
    ResNet      Skip Connections
    EfficientNet Skalierbare Architektur

  RECURRENT NEURAL NETWORKS (RNN)
  -------------------------------
  Fuer sequentielle Daten (Text, Zeitreihen).

  Varianten:
    Vanilla RNN     Einfach, Vanishing Gradient Problem
    LSTM            Long Short-Term Memory
    GRU             Gated Recurrent Unit (vereinfacht)
    Bidirectional   Verarbeitung in beide Richtungen

  LSTM Zellen:
    Forget Gate     Was vergessen?
    Input Gate      Was speichern?
    Output Gate     Was ausgeben?

  TRANSFORMER
  -----------
  Grundlage moderner Sprachmodelle.

  Kernkomponenten:
    Self-Attention    Beziehungen zwischen allen Tokens
    Multi-Head        Mehrere parallele Attention-Mechanismen
    Positional Enc.   Positionsinformation
    Feed-Forward      Verarbeitung pro Position

  Attention-Mechanismus:
    Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) * V

    Q = Query   (Was suche ich?)
    K = Key     (Was biete ich an?)
    V = Value   (Was liefere ich?)

  Bekannte Modelle:
    BERT        Bidirectional, Masked LM
    GPT         Autoregressive, Generativ
    T5          Text-to-Text
    LLaMA       Meta's Open Source

LARGE LANGUAGE MODELS (LLMs)
============================

  UEBERBLICK
  ----------
  Grosse Transformer-Modelle, trainiert auf riesigen Textmengen.

  Eigenschaften:
    - Milliarden von Parametern
    - Emergent Abilities bei Skalierung
    - Few-Shot und Zero-Shot Learning
    - Generative Faehigkeiten

  BEKANNTE MODELLE
  ----------------
    GPT-4       OpenAI, Multimodal
    Claude      Anthropic, Sicherheitsfokus
    Gemini      Google, Multimodal
    LLaMA       Meta, Open Source
    Mistral     Mistral AI, Effizient
    Command R   Cohere, Enterprise

  TRAININGSVERFAHREN
  ------------------
    Pre-Training       Grosse Textmengen, Next Token Prediction
    Fine-Tuning        Anpassung an spezifische Aufgabe
    RLHF               Reinforcement Learning from Human Feedback
    Constitutional AI  KI trainiert sich an Prinzipien

  ANWENDUNGEN
  -----------
    - Chatbots und Assistenten
    - Textgenerierung
    - Code-Generierung
    - Uebersetzung
    - Zusammenfassung
    - Frage-Antwort-Systeme

  PROMPT ENGINEERING
  ------------------
  Techniken zur effektiven LLM-Nutzung:

    Zero-Shot       Direkte Anfrage ohne Beispiele
    Few-Shot        Beispiele im Prompt
    Chain-of-Thought   Schritt-fuer-Schritt Reasoning
    System Prompts     Rollenkontext setzen
    Output Formatting  Strukturierte Ausgabe

COMPUTER VISION
===============

  AUFGABEN
  --------
    Image Classification   Bild einer Kategorie zuordnen
    Object Detection       Objekte lokalisieren und klassifizieren
    Semantic Segmentation  Pixel-genaue Klassifikation
    Instance Segmentation  Objekt-Instanzen unterscheiden
    Pose Estimation        Koerperhaltung erkennen
    Face Recognition       Gesichtserkennung

  MODELLE UND TOOLS
  -----------------
    YOLO          Real-time Object Detection
    Mask R-CNN    Instance Segmentation
    ViT           Vision Transformer
    CLIP          Text-Bild Verknuepfung
    SAM           Segment Anything Model

NATURAL LANGUAGE PROCESSING (NLP)
=================================

  AUFGABEN
  --------
    Tokenization        Text in Tokens zerlegen
    Named Entity Rec.   Entitaeten erkennen (Personen, Orte)
    Sentiment Analysis  Stimmung analysieren
    Machine Translation Uebersetzung
    Summarization       Zusammenfassung
    Question Answering  Fragebeantwortung
    Text Generation     Textgenerierung

  TECHNIKEN
  ---------
    Word Embeddings     Word2Vec, GloVe
    Contextual Emb.     BERT, GPT
    Attention           Transformer-Basis
    RAG                 Retrieval Augmented Generation

FRAMEWORKS UND TOOLS
====================

  PYTHON BIBLIOTHEKEN
  -------------------
    NumPy         Numerische Berechnungen
    Pandas        Datenmanipulation
    scikit-learn  Klassische ML-Algorithmen

  DEEP LEARNING FRAMEWORKS
  ------------------------
    PyTorch       Meta, Forschungsstandard
    TensorFlow    Google, Production-fokussiert
    JAX           Google, Funktional
    Keras         High-Level API

  SPEZIALISIERTE TOOLS
  --------------------
    Hugging Face  Transformers, Datasets, Hub
    LangChain     LLM-Anwendungen
    spaCy         NLP Pipeline
    OpenCV        Computer Vision

BEISPIEL: KLASSIFIKATION MIT PYTORCH
====================================

    import torch
    import torch.nn as nn
    from torch.utils.data import DataLoader

    # Modell definieren
    class Classifier(nn.Module):
        def __init__(self, input_size, hidden_size, num_classes):
            super().__init__()
            self.layers = nn.Sequential(
                nn.Linear(input_size, hidden_size),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(hidden_size, hidden_size),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(hidden_size, num_classes)
            )

        def forward(self, x):
            return self.layers(x)

    # Training
    model = Classifier(784, 256, 10)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(10):
        for batch_x, batch_y in dataloader:
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()

BEISPIEL: HUGGING FACE TRANSFORMER
==================================

    from transformers import pipeline

    # Sentiment Analysis
    classifier = pipeline("sentiment-analysis")
    result = classifier("I love this product!")
    # [{'label': 'POSITIVE', 'score': 0.99}]

    # Text Generation
    generator = pipeline("text-generation", model="gpt2")
    text = generator("The future of AI is", max_length=50)

    # Question Answering
    qa = pipeline("question-answering")
    answer = qa(
        question="What is the capital of France?",
        context="France is a country in Europe. Paris is its capital."
    )

BEST PRACTICES
==============

  DATEN
  -----
    - Qualitaet vor Quantitaet
    - Train/Validation/Test Split (70/15/15)
    - Data Augmentation nutzen
    - Auf Bias pruefen

  TRAINING
  --------
    - Mit kleinem Modell starten
    - Learning Rate Scheduler
    - Early Stopping bei Overfitting
    - Checkpoints speichern

  EVALUATION
  ----------
    - Mehrere Metriken betrachten
    - Confusion Matrix analysieren
    - Kreuzvalidierung nutzen
    - Real-World Testing

  DEPLOYMENT
  ----------
    - Model Quantization fuer Effizienz
    - ONNX fuer Portabilitaet
    - Monitoring in Produktion
    - Drift Detection

ETHIK UND VERANTWORTUNG
=======================

  BIAS
  ----
  ML-Modelle koennen Vorurteile aus Trainingsdaten lernen.
    - Diverse Datensaetze nutzen
    - Fairness-Metriken pruefen
    - Regelmaessige Audits

  TRANSPARENZ
  -----------
    - Erklaerbare KI (XAI)
    - Dokumentation der Grenzen
    - Offenlegung bei KI-Nutzung

  SICHERHEIT
  ----------
    - Adversarial Attacks bedenken
    - Prompt Injection verhindern
    - Datenschutz (DSGVO)

SIEHE AUCH
==========
  wiki/ai_portable.txt
  wiki/informatik/algorithmen/README.txt
  wiki/python/datenanalyse/README.txt
  wiki/automatisierung/README.txt
