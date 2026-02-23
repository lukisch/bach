# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: NumPy/Pandas Dokumentation, Real Python, Towards Data Science

DATENANALYSE MIT PYTHON
=======================

Stand: 2026-02-05

UEBERBLICK
==========
  Python ist die fuehrende Sprache fuer Datenanalyse.
  Kernbibliotheken: NumPy und Pandas.

  Oekosystem:
    NumPy      - Numerische Berechnungen, Arrays
    Pandas     - Datenstrukturen, Analyse
    Matplotlib - Visualisierung (Basis)
    Seaborn    - Statistische Visualisierung
    SciPy      - Wissenschaftliche Berechnungen
    Scikit-learn - Machine Learning

NUMPY - NUMERISCHE GRUNDLAGE
============================

  INSTALLATION
  ------------
    pip install numpy

  IMPORT-KONVENTION
  -----------------
    import numpy as np

  ARRAYS ERSTELLEN
  ----------------
    # Aus Liste
    arr = np.array([1, 2, 3, 4, 5])

    # Mehrdimensional
    matrix = np.array([[1, 2, 3], [4, 5, 6]])

    # Spezielle Arrays
    zeros = np.zeros((3, 4))        # 3x4 Nullen
    ones = np.ones((2, 3))          # 2x3 Einsen
    eye = np.eye(4)                 # 4x4 Einheitsmatrix
    arange = np.arange(0, 10, 2)    # [0, 2, 4, 6, 8]
    linspace = np.linspace(0, 1, 5) # 5 Werte zwischen 0 und 1

  ARRAY-EIGENSCHAFTEN
  -------------------
    arr.shape       # Dimensionen (3, 4)
    arr.ndim        # Anzahl Dimensionen
    arr.size        # Gesamtzahl Elemente
    arr.dtype       # Datentyp (float64, int32, ...)

  INDIZIERUNG UND SLICING
  -----------------------
    arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    arr[0]          # Erste Zeile: [1, 2, 3]
    arr[0, 1]       # Element Zeile 0, Spalte 1: 2
    arr[:, 0]       # Erste Spalte: [1, 4, 7]
    arr[0:2, 1:3]   # Teilmatrix
    arr[arr > 5]    # Boolean Indexing: [6, 7, 8, 9]

  MATHEMATISCHE OPERATIONEN
  -------------------------
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])

    # Elementweise
    a + b           # [5, 7, 9]
    a * b           # [4, 10, 18]
    a ** 2          # [1, 4, 9]
    np.sqrt(a)      # [1.0, 1.41, 1.73]

    # Aggregationen
    np.sum(a)       # 6
    np.mean(a)      # 2.0
    np.std(a)       # Standardabweichung
    np.min(a)       # 1
    np.max(a)       # 3

  MATRIX-OPERATIONEN
  ------------------
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])

    np.dot(A, B)    # Matrixmultiplikation
    A @ B           # Kurzform (Python 3.5+)
    A.T             # Transponierte
    np.linalg.inv(A)  # Inverse
    np.linalg.det(A)  # Determinante

  RESHAPING
  ---------
    arr = np.arange(12)
    arr.reshape(3, 4)   # 3x4 Matrix
    arr.reshape(2, -1)  # 2 Zeilen, Spalten automatisch
    arr.flatten()       # Zurueck zu 1D

  BROADCASTING
  ------------
    # NumPy erweitert automatisch kleinere Arrays
    matrix = np.ones((3, 3))
    row = np.array([1, 2, 3])
    matrix + row        # Addiert row zu jeder Zeile

  RANDOM
  ------
    np.random.seed(42)              # Reproduzierbarkeit
    np.random.rand(3, 3)            # Uniform [0, 1)
    np.random.randn(3, 3)           # Normalverteilt
    np.random.randint(0, 10, (3, 3)) # Ganzzahlen
    np.random.choice([1, 2, 3], 5)  # Zufaellige Auswahl

PANDAS - DATENANALYSE-KRAFTWERK
===============================

  INSTALLATION
  ------------
    pip install pandas

  IMPORT-KONVENTION
  -----------------
    import pandas as pd

  DATENSTRUKTUREN
  ---------------
    Series:    1D, indiziert (wie Dict)
    DataFrame: 2D, Tabelle (wie Excel/SQL)

  SERIES ERSTELLEN
  ----------------
    s = pd.Series([1, 2, 3, 4])
    s = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
    s = pd.Series({'a': 1, 'b': 2, 'c': 3})

  DATAFRAME ERSTELLEN
  -------------------
    # Aus Dictionary
    df = pd.DataFrame({
        'Name': ['Anna', 'Ben', 'Clara'],
        'Alter': [25, 30, 28],
        'Stadt': ['Berlin', 'Hamburg', 'Muenchen']
    })

    # Aus Liste von Dicts
    data = [
        {'Name': 'Anna', 'Alter': 25},
        {'Name': 'Ben', 'Alter': 30}
    ]
    df = pd.DataFrame(data)

  DATEN EINLESEN
  --------------
    # CSV
    df = pd.read_csv('daten.csv')
    df = pd.read_csv('daten.csv', sep=';', encoding='utf-8')

    # Excel
    df = pd.read_excel('daten.xlsx', sheet_name='Tabelle1')

    # JSON
    df = pd.read_json('daten.json')

    # SQL
    import sqlite3
    conn = sqlite3.connect('datenbank.db')
    df = pd.read_sql('SELECT * FROM tabelle', conn)

  DATEN SPEICHERN
  ---------------
    df.to_csv('output.csv', index=False)
    df.to_excel('output.xlsx', index=False)
    df.to_json('output.json', orient='records')

  DATEN ERKUNDEN
  --------------
    df.head()           # Erste 5 Zeilen
    df.tail(10)         # Letzte 10 Zeilen
    df.shape            # (Zeilen, Spalten)
    df.columns          # Spaltennamen
    df.dtypes           # Datentypen
    df.info()           # Uebersicht
    df.describe()       # Statistiken

  SPALTEN AUSWAEHLEN
  ------------------
    df['Name']              # Eine Spalte (Series)
    df[['Name', 'Alter']]   # Mehrere Spalten (DataFrame)
    df.Name                 # Attribut-Zugriff (wenn moeglich)

  ZEILEN AUSWAEHLEN
  -----------------
    df.loc[0]               # Nach Label/Index
    df.loc[0:2]             # Zeilen 0 bis 2
    df.loc[0, 'Name']       # Spezifische Zelle
    df.iloc[0]              # Nach Position
    df.iloc[0:2, 1:3]       # Zeilen 0-1, Spalten 1-2

  FILTERN
  -------
    df[df['Alter'] > 25]
    df[df['Stadt'] == 'Berlin']
    df[(df['Alter'] > 25) & (df['Stadt'] == 'Berlin')]
    df[df['Name'].isin(['Anna', 'Ben'])]
    df[df['Name'].str.contains('a', case=False)]

  SORTIEREN
  ---------
    df.sort_values('Alter')
    df.sort_values('Alter', ascending=False)
    df.sort_values(['Stadt', 'Alter'])

  NEUE SPALTEN
  ------------
    df['Geburtsjahr'] = 2026 - df['Alter']
    df['Volljaehrig'] = df['Alter'] >= 18
    df['Name_Upper'] = df['Name'].str.upper()

  FEHLENDE WERTE
  --------------
    df.isna()               # Boolean-Matrix
    df.isna().sum()         # Anzahl NaN pro Spalte
    df.dropna()             # Zeilen mit NaN entfernen
    df.dropna(subset=['Name'])  # Nur bei bestimmten Spalten
    df.fillna(0)            # NaN durch 0 ersetzen
    df.fillna(method='ffill')   # Forward Fill
    df['Alter'].fillna(df['Alter'].mean())  # Mit Mittelwert

  GRUPPIEREN (GROUPBY)
  --------------------
    # Aggregation
    df.groupby('Stadt')['Alter'].mean()
    df.groupby('Stadt').agg({
        'Alter': ['mean', 'min', 'max'],
        'Name': 'count'
    })

    # Multiple Grouping
    df.groupby(['Stadt', 'Geschlecht'])['Gehalt'].mean()

  PIVOT TABELLEN
  --------------
    pivot = df.pivot_table(
        values='Umsatz',
        index='Monat',
        columns='Produkt',
        aggfunc='sum'
    )

  MERGE/JOIN
  ----------
    # SQL-aehnliches Merging
    merged = pd.merge(df1, df2, on='ID')
    merged = pd.merge(df1, df2, on='ID', how='left')
    # how: 'inner', 'left', 'right', 'outer'

    # Concatenation
    combined = pd.concat([df1, df2])
    combined = pd.concat([df1, df2], axis=1)  # Spaltenweise

  APPLY
  -----
    # Funktion auf Spalte anwenden
    df['Alter_Kategorie'] = df['Alter'].apply(
        lambda x: 'Jung' if x < 30 else 'Aelter'
    )

    # Auf DataFrame
    df.apply(lambda row: row['A'] + row['B'], axis=1)

  ZEITREIHEN
  ----------
    # Datum parsen
    df['Datum'] = pd.to_datetime(df['Datum_String'])

    # Als Index setzen
    df.set_index('Datum', inplace=True)

    # Resampling
    df.resample('M').mean()     # Monatlich
    df.resample('W').sum()      # Woechentlich

    # Rolling
    df['MA_7'] = df['Wert'].rolling(window=7).mean()

VISUALISIERUNG (KURZUEBERSICHT)
===============================

  MATPLOTLIB
  ----------
    import matplotlib.pyplot as plt

    # Liniendiagramm
    plt.plot(x, y)
    plt.xlabel('X-Achse')
    plt.ylabel('Y-Achse')
    plt.title('Mein Plot')
    plt.show()

    # Histogramm
    plt.hist(data, bins=20)

    # Scatter
    plt.scatter(x, y)

  PANDAS DIREKT
  -------------
    df['Wert'].plot()                  # Linie
    df['Wert'].plot(kind='bar')        # Balken
    df['Wert'].plot(kind='hist')       # Histogramm
    df.plot(x='A', y='B', kind='scatter')

  SEABORN
  -------
    import seaborn as sns

    sns.histplot(df['Alter'])
    sns.boxplot(x='Stadt', y='Alter', data=df)
    sns.heatmap(df.corr(), annot=True)

PERFORMANCE-TIPPS
=================
  1. Vectorized Operations statt Loops
  2. Richtige Datentypen waehlen (category fuer kategorisch)
  3. Chunked Reading fuer grosse Dateien
  4. Nur benoetigte Spalten laden
  5. query() statt Boolean Indexing (bei grossen DataFrames)

  # Beispiel: Kategorisch
  df['Stadt'] = df['Stadt'].astype('category')

  # Chunked Reading
  chunks = pd.read_csv('gross.csv', chunksize=10000)
  for chunk in chunks:
      process(chunk)

BEST PRACTICES
==============
  1. Kopien explizit machen: df_copy = df.copy()
  2. Method Chaining nutzen
  3. Aussagekraeftige Spaltennamen
  4. Index sinnvoll setzen
  5. Docstrings in Analyse-Funktionen
  6. Notebooks fuer explorative Analyse

  # Method Chaining Beispiel
  result = (df
      .query('Alter > 25')
      .groupby('Stadt')
      ['Gehalt']
      .mean()
      .sort_values(ascending=False)
  )

BACH-INTEGRATION
================
  Partner-Zuweisung:
    - Claude: Code-Erklaerung, Analyse-Strategien
    - Gemini: Bibliotheken-Recherche, Visualisierung
    - Ollama: Lokale Datenverarbeitung

  Typische Aufgaben:
    - Daten bereinigen und transformieren
    - Explorative Datenanalyse
    - Visualisierungen erstellen
    - Reports generieren

SIEHE AUCH
==========
  wiki/python/README.txt
  wiki/informatik/programmierung/README.txt
  wiki/it_tools/excel_formeln.txt
