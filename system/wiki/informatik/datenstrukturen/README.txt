================================================================================
                            DATENSTRUKTUREN
                    Organisation und Verwaltung von Daten
================================================================================

Portabilitaet:      UNIVERSAL
Zuletzt validiert:  2026-02-05
Naechste Pruefung:  2027-02-05
Quellen:            Cormen et al. "Introduction to Algorithms" (4th Ed.),
                    Sedgewick "Algorithms" (4th Ed.),
                    Goodrich & Tamassia "Data Structures and Algorithms"

Stand: 2026-02-05

================================================================================
                              EINFUEHRUNG
================================================================================

Eine Datenstruktur ist eine spezielle Art der Speicherung und Organisation von
Daten in einem Computer, die effizienten Zugriff und Modifikation ermoeglicht.
Die Wahl der richtigen Datenstruktur ist entscheidend fuer die Effizienz von
Algorithmen.

KRITERIEN FUER DIE WAHL
-----------------------
  - Art der Operationen (Einfuegen, Loeschen, Suchen, Sortieren)
  - Haeufigkeit der Operationen
  - Speicherplatzbedarf
  - Komplexitaet der Implementierung
  - Ordnungserhaltung der Daten

ABSTRAKTE DATENTYPEN (ADT) VS. DATENSTRUKTUREN
----------------------------------------------
  ADT:            Definiert Operationen und Verhalten (Was)
  Datenstruktur:  Konkrete Implementierung (Wie)

  Beispiel: ADT "Liste" kann als Array oder verkettete Liste implementiert werden

================================================================================
                          LINEARE STRUKTUREN
================================================================================

ARRAYS (FELDER)
---------------
Ein Array ist eine zusammenhaengende Folge von Elementen gleichen Typs mit
festem Index-Zugriff.

Eigenschaften:
  - Feste Groesse (bei statischen Arrays)
  - Direkter Zugriff ueber Index in O(1)
  - Elemente im Speicher zusammenhaengend

Operationen und Komplexitaet:
  Operation          | Komplexitaet
  -------------------|-------------
  Zugriff (Index)    | O(1)
  Suche (unsortiert) | O(n)
  Suche (sortiert)   | O(log n)
  Einfuegen (Ende)   | O(1) amortisiert (dynamisch)
  Einfuegen (Mitte)  | O(n)
  Loeschen (Ende)    | O(1)
  Loeschen (Mitte)   | O(n)

Pseudocode - Dynamisches Array (Verdopplung):
  PROCEDURE append(A, element)
      IF size == capacity THEN
          newCapacity = capacity * 2
          Erstelle neues Array B mit newCapacity
          Kopiere alle Elemente von A nach B
          A = B
      END IF
      A[size] = element
      size = size + 1
  END PROCEDURE

VERKETTETE LISTEN
-----------------
Eine verkettete Liste besteht aus Knoten, die Daten und Zeiger auf
Nachfolger (und ggf. Vorgaenger) enthalten.

Typen:
  - Einfach verkettet: Jeder Knoten zeigt auf Nachfolger
  - Doppelt verkettet: Zeiger auf Nachfolger und Vorgaenger
  - Zirkulaer verkettet: Letzter Knoten zeigt auf ersten

Struktur eines Knotens (einfach verkettet):
  STRUCTURE Node
      data: ANY
      next: POINTER TO Node
  END STRUCTURE

Operationen und Komplexitaet:
  Operation                | Einfach   | Doppelt
  -------------------------|-----------|--------
  Zugriff (Index)          | O(n)      | O(n)
  Suche                    | O(n)      | O(n)
  Einfuegen (Anfang)       | O(1)      | O(1)
  Einfuegen (Ende)         | O(n)*     | O(1)**
  Einfuegen (Mitte)        | O(1)***   | O(1)***
  Loeschen (Anfang)        | O(1)      | O(1)
  Loeschen (Ende)          | O(n)      | O(1)
  Loeschen (Mitte)         | O(1)***   | O(1)***

  *  O(1) mit Tail-Pointer
  ** Mit Tail-Pointer
  *** Nach dem Finden des Knotens

Pseudocode - Einfuegen am Anfang:
  PROCEDURE insertAtHead(list, value)
      newNode = CREATE Node(value)
      newNode.next = list.head
      list.head = newNode
  END PROCEDURE

Pseudocode - Loeschen eines Knotens:
  PROCEDURE deleteNode(list, value)
      IF list.head == NULL THEN RETURN
      IF list.head.data == value THEN
          list.head = list.head.next
          RETURN
      END IF
      current = list.head
      WHILE current.next != NULL DO
          IF current.next.data == value THEN
              current.next = current.next.next
              RETURN
          END IF
          current = current.next
      END WHILE
  END PROCEDURE

================================================================================
                          STACKS UND QUEUES
================================================================================

STACK (STAPEL) - LIFO
---------------------
Last In, First Out: Das zuletzt eingefuegte Element wird zuerst entfernt.

Operationen:
  - push(element)   : Element auf Stack legen          O(1)
  - pop()           : Oberstes Element entfernen       O(1)
  - peek() / top()  : Oberstes Element ansehen         O(1)
  - isEmpty()       : Pruefen ob leer                  O(1)

Pseudocode (Array-Implementierung):
  STRUCTURE Stack
      array: ARRAY
      top: INTEGER = -1
  END STRUCTURE

  PROCEDURE push(stack, element)
      stack.top = stack.top + 1
      stack.array[stack.top] = element
  END PROCEDURE

  FUNCTION pop(stack)
      IF stack.top < 0 THEN
          ERROR "Stack Underflow"
      END IF
      element = stack.array[stack.top]
      stack.top = stack.top - 1
      RETURN element
  END FUNCTION

Anwendungen:
  - Funktionsaufrufe (Call Stack)
  - Undo-Operationen in Editoren
  - Klammervalidierung
  - Auswertung von Ausdruecken (Postfix-Notation)
  - Backtracking-Algorithmen

Beispiel - Klammervalidierung:
  FUNCTION isBalanced(expression)
      stack = CREATE Stack
      FOR EACH char IN expression DO
          IF char IN ['(', '[', '{'] THEN
              stack.push(char)
          ELSE IF char IN [')', ']', '}'] THEN
              IF stack.isEmpty() THEN RETURN FALSE
              top = stack.pop()
              IF NOT matching(top, char) THEN RETURN FALSE
          END IF
      END FOR
      RETURN stack.isEmpty()
  END FUNCTION

QUEUE (WARTESCHLANGE) - FIFO
----------------------------
First In, First Out: Das zuerst eingefuegte Element wird zuerst entfernt.

Operationen:
  - enqueue(element) : Element hinten anfuegen         O(1)
  - dequeue()        : Vorderstes Element entfernen    O(1)
  - front() / peek() : Vorderstes Element ansehen      O(1)
  - isEmpty()        : Pruefen ob leer                 O(1)

Pseudocode (Zirkulaeres Array):
  STRUCTURE Queue
      array: ARRAY[0..capacity-1]
      front: INTEGER = 0
      rear: INTEGER = -1
      size: INTEGER = 0
  END STRUCTURE

  PROCEDURE enqueue(queue, element)
      IF queue.size == capacity THEN
          ERROR "Queue Overflow"
      END IF
      queue.rear = (queue.rear + 1) MOD capacity
      queue.array[queue.rear] = element
      queue.size = queue.size + 1
  END PROCEDURE

  FUNCTION dequeue(queue)
      IF queue.size == 0 THEN
          ERROR "Queue Underflow"
      END IF
      element = queue.array[queue.front]
      queue.front = (queue.front + 1) MOD capacity
      queue.size = queue.size - 1
      RETURN element
  END FUNCTION

Varianten:
  - Deque (Double-Ended Queue): Einfuegen/Entfernen an beiden Enden
  - Priority Queue: Elemente nach Prioritaet sortiert
  - Circular Queue: Effiziente Array-Implementierung

Anwendungen:
  - Warteschlangen in Betriebssystemen (Prozess-Scheduling)
  - Breitensuche (BFS) in Graphen
  - Drucker-Warteschlangen
  - Puffer fuer Datenstreams

================================================================================
                              BAEUME
================================================================================

Ein Baum ist eine hierarchische Datenstruktur mit Knoten, die durch
Kanten verbunden sind. Ein Baum hat genau eine Wurzel und keine Zyklen.

TERMINOLOGIE
------------
  - Wurzel (Root):     Oberster Knoten ohne Elternknoten
  - Blatt (Leaf):      Knoten ohne Kinder
  - Innerer Knoten:    Knoten mit mindestens einem Kind
  - Tiefe (Depth):     Abstand eines Knotens zur Wurzel
  - Hoehe (Height):    Maximale Tiefe aller Blaetter
  - Grad (Degree):     Anzahl der Kinder eines Knotens

BINAERBAUM
----------
Jeder Knoten hat maximal zwei Kinder (links und rechts).

Struktur:
  STRUCTURE BinaryNode
      data: ANY
      left: POINTER TO BinaryNode
      right: POINTER TO BinaryNode
  END STRUCTURE

Traversierungen:
  - Inorder (LWR):   Links -> Wurzel -> Rechts
  - Preorder (WLR):  Wurzel -> Links -> Rechts
  - Postorder (LRW): Links -> Rechts -> Wurzel
  - Level-Order:     Ebene fuer Ebene (mit Queue)

Pseudocode - Inorder-Traversierung:
  PROCEDURE inorder(node)
      IF node != NULL THEN
          inorder(node.left)
          PRINT node.data
          inorder(node.right)
      END IF
  END PROCEDURE

BINAERER SUCHBAUM (BST)
-----------------------
Ein binaerer Suchbaum erfuellt die BST-Eigenschaft:
  - Alle Knoten im linken Teilbaum < Wurzel
  - Alle Knoten im rechten Teilbaum > Wurzel

Operationen und Komplexitaet:
  Operation    | Average   | Worst (entartet)
  -------------|-----------|------------------
  Suche        | O(log n)  | O(n)
  Einfuegen    | O(log n)  | O(n)
  Loeschen     | O(log n)  | O(n)
  Min/Max      | O(log n)  | O(n)

Pseudocode - Suche im BST:
  FUNCTION search(node, key)
      IF node == NULL OR node.data == key THEN
          RETURN node
      END IF
      IF key < node.data THEN
          RETURN search(node.left, key)
      ELSE
          RETURN search(node.right, key)
      END IF
  END FUNCTION

BALANCIERTE BAEUME
------------------

AVL-Baum:
  - Hoehendifferenz zwischen linkem und rechtem Teilbaum <= 1
  - Rebalancierung durch Rotationen
  - Garantiert O(log n) fuer alle Operationen

Red-Black-Baum:
  - Knoten sind rot oder schwarz gefaerbt
  - Wurzel und Blaetter (NIL) sind schwarz
  - Rote Knoten haben schwarze Kinder
  - Gleiche Anzahl schwarzer Knoten auf allen Pfaden
  - Garantiert O(log n), etwas schneller bei Einfuegen/Loeschen

HEAP
----
Ein Heap ist ein vollstaendiger Binaerbaum mit Heap-Eigenschaft.

  - Max-Heap: Elternknoten >= Kinder
  - Min-Heap: Elternknoten <= Kinder

Array-Darstellung (Index ab 0):
  - Elternknoten von i: (i-1) / 2
  - Linkes Kind von i:  2*i + 1
  - Rechtes Kind von i: 2*i + 2

Operationen:
  - insert()      : O(log n)
  - extractMax()  : O(log n)
  - getMax()      : O(1)
  - heapify()     : O(log n)
  - buildHeap()   : O(n)

TRIE (PRAEFIXBAUM)
------------------
Spezieller Baum fuer Zeichenketten, bei dem jeder Pfad von der Wurzel
ein Praefix repraesentiert.

Anwendungen:
  - Autovervollstaendigung
  - Rechtschreibpruefung
  - IP-Routing (Longest Prefix Matching)

Komplexitaet (m = Laenge der Zeichenkette):
  - Einfuegen: O(m)
  - Suche:     O(m)
  - Loeschen:  O(m)

================================================================================
                              GRAPHEN
================================================================================

Ein Graph G = (V, E) besteht aus Knoten (Vertices) V und Kanten (Edges) E.

TYPEN
-----
  - Gerichtet:     Kanten haben Richtung (A -> B)
  - Ungerichtet:   Kanten haben keine Richtung (A -- B)
  - Gewichtet:     Kanten haben Gewichte/Kosten
  - Zyklisch:      Enthaelt mindestens einen Zyklus
  - Azyklisch:     Enthaelt keinen Zyklus (DAG bei gerichtet)

DARSTELLUNG
-----------

Adjazenzmatrix:
  - 2D-Array A[i][j] = 1 wenn Kante (i,j) existiert
  - Speicher: O(V^2)
  - Kantenabfrage: O(1)
  - Alle Nachbarn: O(V)

Adjazenzliste:
  - Array von Listen: Jeder Knoten speichert seine Nachbarn
  - Speicher: O(V + E)
  - Kantenabfrage: O(Grad des Knotens)
  - Alle Nachbarn: O(Grad des Knotens)

Wann was verwenden?
  - Dichte Graphen (viele Kanten):   Adjazenzmatrix
  - Duenne Graphen (wenige Kanten):  Adjazenzliste

Pseudocode - Adjazenzliste:
  STRUCTURE Graph
      numVertices: INTEGER
      adjList: ARRAY OF LIST
  END STRUCTURE

  PROCEDURE addEdge(graph, u, v)
      graph.adjList[u].append(v)
      // Fuer ungerichtete Graphen:
      graph.adjList[v].append(u)
  END PROCEDURE

================================================================================
                          HASH-STRUKTUREN
================================================================================

HASHMAP / HASHTABLE
-------------------
Speichert Key-Value-Paare mit schnellem Zugriff ueber Hashfunktion.

Prinzip:
  1. Hashfunktion berechnet Index aus Key
  2. Wert wird an diesem Index gespeichert
  3. Kollisionen muessen behandelt werden

Operationen (durchschnittlich):
  - put(key, value)  : O(1)
  - get(key)         : O(1)
  - remove(key)      : O(1)
  - containsKey()    : O(1)

Kollisionsbehandlung:

  1. Chaining (Verkettung):
     - Jeder Bucket enthaelt eine Liste
     - Kollidierende Elemente werden an Liste angehaengt

  2. Open Addressing (Offene Adressierung):
     - Linear Probing:    index = (hash + i) % size
     - Quadratic Probing: index = (hash + i^2) % size
     - Double Hashing:    index = (hash1 + i * hash2) % size

Pseudocode - HashMap mit Chaining:
  STRUCTURE HashMap
      buckets: ARRAY OF LIST
      size: INTEGER
  END STRUCTURE

  FUNCTION hash(key)
      RETURN hashCode(key) MOD size
  END FUNCTION

  PROCEDURE put(map, key, value)
      index = hash(key)
      FOR EACH pair IN map.buckets[index] DO
          IF pair.key == key THEN
              pair.value = value
              RETURN
          END IF
      END FOR
      map.buckets[index].append((key, value))
  END PROCEDURE

Load Factor und Rehashing:
  - Load Factor = Anzahl Elemente / Anzahl Buckets
  - Bei hohem Load Factor: Rehashing (Vergroessern und neu einfuegen)
  - Typischer Schwellwert: 0.75

HASHSET
-------
Speichert einzigartige Elemente ohne Duplikate.
Intern oft als HashMap mit Dummy-Werten implementiert.

Operationen:
  - add(element)      : O(1)
  - remove(element)   : O(1)
  - contains(element) : O(1)

================================================================================
                       KOMPLEXITAETSVERGLEICH
================================================================================

  Struktur          | Zugriff   | Suche     | Einfuegen | Loeschen
  ------------------|-----------|-----------|-----------|----------
  Array             | O(1)      | O(n)      | O(n)      | O(n)
  Verkettete Liste  | O(n)      | O(n)      | O(1)*     | O(1)*
  Stack             | O(n)      | O(n)      | O(1)      | O(1)
  Queue             | O(n)      | O(n)      | O(1)      | O(1)
  BST (balanciert)  | O(log n)  | O(log n)  | O(log n)  | O(log n)
  Heap              | O(1)**    | O(n)      | O(log n)  | O(log n)
  HashMap           | O(1)      | O(1)      | O(1)      | O(1)
  HashSet           | -         | O(1)      | O(1)      | O(1)

  *  Nach dem Finden der Position
  ** Nur fuer Max/Min

================================================================================
                         VERFUEGBARE ARTIKEL
================================================================================

  arrays_listen.txt      - Arrays und verkettete Listen im Detail
  stacks_queues.txt      - Stacks, Queues und Varianten
  baeume.txt             - Binaerbaeume, BST, AVL, Heaps
  graphen.txt            - Graphentheorie und Darstellung
  hashmaps.txt           - Hashfunktionen und Kollisionsbehandlung

================================================================================
                            SIEHE AUCH
================================================================================

  wiki/informatik/algorithmen/     - Algorithmen (Sortierung, Suche, etc.)
  wiki/informatik/graphen/         - Graphenalgorithmen (Dijkstra, BFS, DFS)
  wiki/java/collections/           - Java Collections Framework
  wiki/python/datentypen/          - Python Built-in Datenstrukturen

================================================================================
