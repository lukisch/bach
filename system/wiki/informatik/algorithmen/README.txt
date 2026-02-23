================================================================================
                              ALGORITHMEN
                         Grundlagen und Techniken
================================================================================

Portabilitaet:      UNIVERSAL
Zuletzt validiert:  2026-02-05
Naechste Pruefung:  2027-02-05
Quellen:            Cormen et al. "Introduction to Algorithms" (4th Ed.),
                    Sedgewick "Algorithms" (4th Ed.),
                    Knuth "The Art of Computer Programming"

Stand: 2026-02-05

================================================================================
                              EINFUEHRUNG
================================================================================

Ein Algorithmus ist eine endliche, eindeutige Folge von Anweisungen zur Loesung
eines Problems oder einer Klasse von Problemen. Der Begriff stammt vom
persischen Mathematiker al-Chwarizmi (9. Jahrhundert).

EIGENSCHAFTEN EINES ALGORITHMUS
-------------------------------
  1. Finitheit       - Endliche Anzahl von Schritten
  2. Determiniertheit - Gleiche Eingabe ergibt gleiche Ausgabe
  3. Determinismus   - Jeder Schritt ist eindeutig definiert
  4. Effektivitaet   - Jeder Schritt ist ausfuehrbar
  5. Terminierung    - Der Algorithmus endet nach endlicher Zeit

================================================================================
                           KOMPLEXITAETSANALYSE
================================================================================

Die Komplexitaetsanalyse bewertet Algorithmen nach Ressourcenverbrauch
(Zeit und Speicher) in Abhaengigkeit von der Eingabegroesse n.

BIG-O NOTATION (ASYMPTOTISCHE OBERGRENZE)
-----------------------------------------
Die Big-O Notation beschreibt das Wachstumsverhalten im Worst-Case.

  Notation      | Name            | Beispiel
  --------------|-----------------|----------------------------------
  O(1)          | Konstant        | Array-Indexzugriff
  O(log n)      | Logarithmisch   | Binaere Suche
  O(n)          | Linear          | Lineare Suche
  O(n log n)    | Linearithmisch  | Merge Sort, Quick Sort (avg)
  O(n^2)        | Quadratisch     | Bubble Sort, Selection Sort
  O(n^3)        | Kubisch         | Matrix-Multiplikation (naiv)
  O(2^n)        | Exponentiell    | Travelling Salesman (brute force)
  O(n!)         | Faktoriell      | Permutationen

WEITERE NOTATIONEN
------------------
  - Omega (Untergrenze): Der Algorithmus braucht MINDESTENS diese Zeit
  - Theta (Exakte Grenze): Ober- und Untergrenze stimmen ueberein
  - Amortisierte Analyse: Durchschnitt ueber Sequenz von Operationen

BEISPIEL: KOMPLEXITAETSBERECHNUNG
---------------------------------
  PROCEDURE beispiel(n)
      FOR i = 1 TO n DO           // n Iterationen
          FOR j = 1 TO n DO       // n Iterationen
              PRINT i, j          // O(1)
          END FOR
      END FOR
  END PROCEDURE

  Analyse: n * n * O(1) = O(n^2)

================================================================================
                           SORTIERALGORITHMEN
================================================================================

EINFACHE SORTIERALGORITHMEN
---------------------------

BUBBLE SORT
  Prinzip:    Wiederholtes Vertauschen benachbarter Elemente
  Komplexitaet: Zeit O(n^2), Speicher O(1)
  Stabil:     Ja

  PROCEDURE bubbleSort(A[0..n-1])
      FOR i = 0 TO n-2 DO
          FOR j = 0 TO n-2-i DO
              IF A[j] > A[j+1] THEN
                  SWAP(A[j], A[j+1])
              END IF
          END FOR
      END FOR
  END PROCEDURE

SELECTION SORT
  Prinzip:    Minimum finden und an richtige Position setzen
  Komplexitaet: Zeit O(n^2), Speicher O(1)
  Stabil:     Nein

  PROCEDURE selectionSort(A[0..n-1])
      FOR i = 0 TO n-2 DO
          minIndex = i
          FOR j = i+1 TO n-1 DO
              IF A[j] < A[minIndex] THEN
                  minIndex = j
              END IF
          END FOR
          SWAP(A[i], A[minIndex])
      END FOR
  END PROCEDURE

INSERTION SORT
  Prinzip:    Elemente nacheinander in sortierte Teilfolge einfuegen
  Komplexitaet: Zeit O(n^2), Speicher O(1)
  Stabil:     Ja
  Hinweis:    Effizient fuer kleine oder fast sortierte Arrays

  PROCEDURE insertionSort(A[0..n-1])
      FOR i = 1 TO n-1 DO
          key = A[i]
          j = i - 1
          WHILE j >= 0 AND A[j] > key DO
              A[j+1] = A[j]
              j = j - 1
          END WHILE
          A[j+1] = key
      END FOR
  END PROCEDURE

EFFIZIENTE SORTIERALGORITHMEN
-----------------------------

MERGE SORT (Divide and Conquer)
  Prinzip:    Array teilen, rekursiv sortieren, zusammenfuehren
  Komplexitaet: Zeit O(n log n), Speicher O(n)
  Stabil:     Ja

  PROCEDURE mergeSort(A, left, right)
      IF left < right THEN
          mid = (left + right) / 2
          mergeSort(A, left, mid)
          mergeSort(A, mid+1, right)
          merge(A, left, mid, right)
      END IF
  END PROCEDURE

  PROCEDURE merge(A, left, mid, right)
      // Erstelle temporaere Arrays L und R
      // Kopiere Elemente
      // Fuege sortiert zurueck in A
  END PROCEDURE

QUICK SORT
  Prinzip:    Pivot waehlen, partitionieren, rekursiv sortieren
  Komplexitaet: Zeit O(n log n) avg, O(n^2) worst, Speicher O(log n)
  Stabil:     Nein

  PROCEDURE quickSort(A, low, high)
      IF low < high THEN
          pivotIndex = partition(A, low, high)
          quickSort(A, low, pivotIndex - 1)
          quickSort(A, pivotIndex + 1, high)
      END IF
  END PROCEDURE

  PROCEDURE partition(A, low, high)
      pivot = A[high]
      i = low - 1
      FOR j = low TO high - 1 DO
          IF A[j] <= pivot THEN
              i = i + 1
              SWAP(A[i], A[j])
          END IF
      END FOR
      SWAP(A[i+1], A[high])
      RETURN i + 1
  END PROCEDURE

HEAP SORT
  Prinzip:    Array als Heap organisieren, Maximum extrahieren
  Komplexitaet: Zeit O(n log n), Speicher O(1)
  Stabil:     Nein

================================================================================
                            SUCHALGORITHMEN
================================================================================

LINEARE SUCHE
-------------
  Komplexitaet: Zeit O(n), Speicher O(1)
  Voraussetzung: Keine

  PROCEDURE linearSearch(A[0..n-1], target)
      FOR i = 0 TO n-1 DO
          IF A[i] == target THEN
              RETURN i
          END IF
      END FOR
      RETURN -1  // Nicht gefunden
  END PROCEDURE

BINAERE SUCHE
-------------
  Komplexitaet: Zeit O(log n), Speicher O(1) iterativ, O(log n) rekursiv
  Voraussetzung: Sortiertes Array

  PROCEDURE binarySearch(A[0..n-1], target)
      left = 0
      right = n - 1
      WHILE left <= right DO
          mid = left + (right - left) / 2
          IF A[mid] == target THEN
              RETURN mid
          ELSE IF A[mid] < target THEN
              left = mid + 1
          ELSE
              right = mid - 1
          END IF
      END WHILE
      RETURN -1  // Nicht gefunden
  END PROCEDURE

GRAPHENSUCHE: BREITENSUCHE (BFS)
--------------------------------
  Komplexitaet: Zeit O(V + E), Speicher O(V)
  Eigenschaften: Findet kuerzesten Pfad (ungewichteter Graph)

  PROCEDURE BFS(Graph G, startVertex s)
      Erstelle Queue Q
      Markiere s als besucht
      Q.enqueue(s)
      WHILE NOT Q.isEmpty() DO
          v = Q.dequeue()
          Verarbeite v
          FOR EACH Nachbar w von v DO
              IF w nicht besucht THEN
                  Markiere w als besucht
                  Q.enqueue(w)
              END IF
          END FOR
      END WHILE
  END PROCEDURE

GRAPHENSUCHE: TIEFENSUCHE (DFS)
-------------------------------
  Komplexitaet: Zeit O(V + E), Speicher O(V)
  Eigenschaften: Gut fuer Zykluserkennung, topologische Sortierung

  PROCEDURE DFS(Graph G, vertex v)
      Markiere v als besucht
      Verarbeite v
      FOR EACH Nachbar w von v DO
          IF w nicht besucht THEN
              DFS(G, w)
          END IF
      END FOR
  END PROCEDURE

================================================================================
                              REKURSION
================================================================================

Rekursion ist eine Technik, bei der eine Funktion sich selbst aufruft.

STRUKTUR EINER REKURSIVEN FUNKTION
----------------------------------
  1. Basisfall(e)     - Beendet die Rekursion
  2. Rekursionsfall   - Reduziert das Problem, ruft sich selbst auf

BEISPIEL: FAKULTAET
-------------------
  FUNCTION factorial(n)
      IF n <= 1 THEN           // Basisfall
          RETURN 1
      ELSE
          RETURN n * factorial(n - 1)  // Rekursionsfall
      END IF
  END FUNCTION

  Aufrufkette fuer factorial(4):
    factorial(4) = 4 * factorial(3)
                 = 4 * 3 * factorial(2)
                 = 4 * 3 * 2 * factorial(1)
                 = 4 * 3 * 2 * 1
                 = 24

TAIL RECURSION (ENDREKURSION)
-----------------------------
Bei Tail Recursion ist der rekursive Aufruf die letzte Operation.
Ermoeglicht Compiler-Optimierung (Tail Call Optimization).

  FUNCTION factorialTail(n, accumulator)
      IF n <= 1 THEN
          RETURN accumulator
      ELSE
          RETURN factorialTail(n - 1, n * accumulator)
      END IF
  END FUNCTION

  // Aufruf: factorialTail(5, 1)

================================================================================
                       DYNAMISCHE PROGRAMMIERUNG
================================================================================

Dynamische Programmierung (DP) loest Probleme durch Zerlegung in
ueberlappende Teilprobleme und Speichern von Zwischenergebnissen.

ZWEI ANSAETZE
-------------
  1. Top-Down (Memoization): Rekursiv mit Cache
  2. Bottom-Up (Tabulation): Iterativ, Tabelle fuellen

BEISPIEL: FIBONACCI-ZAHLEN

Naive Rekursion O(2^n):
  FUNCTION fib(n)
      IF n <= 1 THEN RETURN n
      RETURN fib(n-1) + fib(n-2)
  END FUNCTION

Memoization O(n):
  FUNCTION fibMemo(n, memo)
      IF n in memo THEN RETURN memo[n]
      IF n <= 1 THEN RETURN n
      memo[n] = fibMemo(n-1, memo) + fibMemo(n-2, memo)
      RETURN memo[n]
  END FUNCTION

Tabulation O(n):
  FUNCTION fibTab(n)
      IF n <= 1 THEN RETURN n
      dp[0] = 0
      dp[1] = 1
      FOR i = 2 TO n DO
          dp[i] = dp[i-1] + dp[i-2]
      END FOR
      RETURN dp[n]
  END FUNCTION

KLASSISCHE DP-PROBLEME
----------------------
  - Rucksackproblem (Knapsack)
  - Laengste gemeinsame Teilfolge (LCS)
  - Kuerzeste Wege (Bellman-Ford, Floyd-Warshall)
  - Matrixkettenmultiplikation
  - Edit Distance (Levenshtein-Distanz)

================================================================================
                          GREEDY-ALGORITHMEN
================================================================================

Greedy-Algorithmen treffen in jedem Schritt die lokal optimale Wahl,
ohne Ruecksicht auf globale Konsequenzen.

EIGENSCHAFTEN
-------------
  - Einfach zu implementieren
  - Oft effizient
  - Nicht immer optimal (funktioniert nur bei bestimmten Problemen)

BEISPIELE
---------

DIJKSTRA'S ALGORITHMUS (Kuerzeste Wege)
  Komplexitaet: O((V + E) log V) mit Priority Queue

  PROCEDURE Dijkstra(Graph G, source s)
      dist[s] = 0
      FOR EACH vertex v != s DO
          dist[v] = INFINITY
      END FOR
      PriorityQueue Q mit allen Knoten
      WHILE NOT Q.isEmpty() DO
          u = Q.extractMin()
          FOR EACH Nachbar v von u DO
              IF dist[u] + weight(u,v) < dist[v] THEN
                  dist[v] = dist[u] + weight(u,v)
                  Q.decreaseKey(v, dist[v])
              END IF
          END FOR
      END WHILE
  END PROCEDURE

HUFFMAN-KODIERUNG (Datenkompression)
  Erstellt optimalen praefixfreien Code basierend auf Zeichenhaeufigkeiten.

AKTIVITAETSAUSWAHL (Activity Selection)
  Waehle maximale Anzahl nicht-ueberlappender Aktivitaeten.

================================================================================
                         DIVIDE AND CONQUER
================================================================================

Teile-und-Herrsche zerlegt ein Problem in kleinere Teilprobleme,
loest diese rekursiv und kombiniert die Loesungen.

SCHEMA
------
  1. DIVIDE:   Problem in Teilprobleme zerlegen
  2. CONQUER:  Teilprobleme rekursiv loesen
  3. COMBINE:  Teilergebnisse zur Gesamtloesung kombinieren

BEISPIELE
---------
  - Merge Sort
  - Quick Sort
  - Binaere Suche
  - Karatsuba-Multiplikation
  - Strassen-Matrixmultiplikation

MASTER-THEOREM
--------------
Fuer Rekurrenzen der Form T(n) = aT(n/b) + f(n):

  Fall 1: f(n) = O(n^(log_b(a) - e))  =>  T(n) = Theta(n^log_b(a))
  Fall 2: f(n) = Theta(n^log_b(a))    =>  T(n) = Theta(n^log_b(a) * log n)
  Fall 3: f(n) = Omega(n^(log_b(a) + e))  =>  T(n) = Theta(f(n))

================================================================================
                        KOMPLEXITAETSVERGLEICH
================================================================================

  Algorithmus          | Best      | Average   | Worst     | Speicher
  ---------------------|-----------|-----------|-----------|----------
  Bubble Sort          | O(n)      | O(n^2)    | O(n^2)    | O(1)
  Selection Sort       | O(n^2)    | O(n^2)    | O(n^2)    | O(1)
  Insertion Sort       | O(n)      | O(n^2)    | O(n^2)    | O(1)
  Merge Sort           | O(n log n)| O(n log n)| O(n log n)| O(n)
  Quick Sort           | O(n log n)| O(n log n)| O(n^2)    | O(log n)
  Heap Sort            | O(n log n)| O(n log n)| O(n log n)| O(1)
  Counting Sort        | O(n + k)  | O(n + k)  | O(n + k)  | O(k)
  Radix Sort           | O(nk)     | O(nk)     | O(nk)     | O(n + k)

================================================================================
                         VERFUEGBARE ARTIKEL
================================================================================

  komplexitaet.txt           - Detaillierte Komplexitaetsanalyse
  sortierung.txt             - Alle Sortieralgorithmen im Detail
  suche.txt                  - Such- und Traversierungsalgorithmen
  rekursion.txt              - Rekursive Techniken und Optimierung
  dynamische_programmierung.txt - DP-Techniken und Beispiele

================================================================================
                            SIEHE AUCH
================================================================================

  wiki/informatik/datenstrukturen/  - Datenstrukturen (Arrays, Listen, etc.)
  wiki/informatik/graphen/          - Graphentheorie und -algorithmen
  wiki/python/funktionen/           - Implementierung in Python
  wiki/java/collections/            - Java Collections Framework

================================================================================
