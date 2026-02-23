JAVA COLLECTIONS
================

# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05
# Naechste Pruefung: 2027-02-05
# Quellen: Oracle Java Documentation, Effective Java (Joshua Bloch)

Stand: 2026-02-05
Status: VOLLSTAENDIG

EINFUEHRUNG
===========
Das Java Collections Framework ist eine einheitliche Architektur zur
Darstellung und Manipulation von Sammlungen (Collections). Es wurde mit
Java 1.2 eingefuehrt und ist ein fundamentaler Bestandteil der Java
Standard Library. Das Framework bietet:

  - Interfaces: Abstrakte Datentypen zur Darstellung von Collections
  - Implementierungen: Konkrete, wiederverwendbare Datenstrukturen
  - Algorithmen: Nuetzliche Methoden wie Sortieren und Suchen

Das Framework befindet sich im Package java.util.

COLLECTION FRAMEWORK HIERARCHIE
===============================
Die Kernstruktur des Frameworks basiert auf Interfaces:

  Iterable<E>
      |
  Collection<E>
      |
      +-- List<E>     (geordnet, erlaubt Duplikate)
      |     +-- ArrayList
      |     +-- LinkedList
      |     +-- Vector (veraltet)
      |
      +-- Set<E>      (einzigartig, keine Duplikate)
      |     +-- HashSet
      |     +-- LinkedHashSet
      |     +-- TreeSet (sortiert)
      |
      +-- Queue<E>    (FIFO-Prinzip)
            +-- LinkedList
            +-- PriorityQueue
            +-- ArrayDeque

  Map<K,V>            (Key-Value Paare, kein Collection-Interface)
      +-- HashMap
      +-- LinkedHashMap
      +-- TreeMap (sortiert)
      +-- Hashtable (veraltet)

LIST - GEORDNETE SAMMLUNG
=========================
Lists speichern Elemente in einer definierten Reihenfolge und erlauben
Duplikate. Zugriff erfolgt ueber Index (0-basiert).

  ARRAYLIST
  ---------
  Basiert auf einem dynamischen Array. Ideal fuer wahlfreien Zugriff.

  Eigenschaften:
    - Zugriff per Index: O(1)
    - Einfuegen am Ende: O(1) amortisiert
    - Einfuegen in der Mitte: O(n)
    - Loeschen: O(n)
    - Nicht synchronisiert

  Codebeispiel:
    import java.util.ArrayList;
    import java.util.List;

    public class ArrayListDemo {
        public static void main(String[] args) {
            List<String> namen = new ArrayList<>();

            // Elemente hinzufuegen
            namen.add("Alice");
            namen.add("Bob");
            namen.add("Charlie");
            namen.add(1, "Zoe");  // An Position 1 einfuegen

            // Zugriff
            String erster = namen.get(0);        // "Alice"
            int index = namen.indexOf("Bob");    // 2

            // Iteration
            for (String name : namen) {
                System.out.println(name);
            }

            // Groesse und Pruefung
            int groesse = namen.size();          // 4
            boolean hatBob = namen.contains("Bob");  // true

            // Entfernen
            namen.remove("Zoe");
            namen.remove(0);  // Entfernt Element an Index 0

            // Initialisierung mit Kapazitaet (Performance)
            List<Integer> zahlen = new ArrayList<>(1000);
        }
    }

  LINKEDLIST
  ----------
  Doppelt verkettete Liste. Ideal fuer haeufiges Einfuegen/Loeschen.

  Eigenschaften:
    - Zugriff per Index: O(n)
    - Einfuegen am Anfang/Ende: O(1)
    - Einfuegen in der Mitte: O(n) (Suche) + O(1) (Einfuegen)
    - Implementiert auch Deque-Interface

  Codebeispiel:
    import java.util.LinkedList;

    LinkedList<String> liste = new LinkedList<>();
    liste.addFirst("Anfang");
    liste.addLast("Ende");
    String kopf = liste.getFirst();
    liste.removeFirst();

SET - EINZIGARTIGE ELEMENTE
===========================
Sets speichern nur einzigartige Elemente. Duplikate werden ignoriert.

  HASHSET
  -------
  Basiert auf HashMap. Keine definierte Reihenfolge.

  Eigenschaften:
    - add(), remove(), contains(): O(1) durchschnittlich
    - Reihenfolge nicht garantiert
    - Erlaubt ein null-Element

  Codebeispiel:
    import java.util.HashSet;
    import java.util.Set;

    public class HashSetDemo {
        public static void main(String[] args) {
            Set<String> farben = new HashSet<>();

            farben.add("Rot");
            farben.add("Blau");
            farben.add("Gruen");
            farben.add("Rot");   // Wird ignoriert (Duplikat)

            System.out.println(farben.size());  // 3

            // Mengenoperationen
            Set<String> andereFarben = new HashSet<>();
            andereFarben.add("Blau");
            andereFarben.add("Gelb");

            // Vereinigung
            Set<String> vereinigung = new HashSet<>(farben);
            vereinigung.addAll(andereFarben);

            // Schnittmenge
            Set<String> schnittmenge = new HashSet<>(farben);
            schnittmenge.retainAll(andereFarben);

            // Differenz
            Set<String> differenz = new HashSet<>(farben);
            differenz.removeAll(andereFarben);
        }
    }

  TREESET
  -------
  Basiert auf Red-Black Tree. Elemente sind sortiert.

  Eigenschaften:
    - Operationen: O(log n)
    - Elemente muessen Comparable implementieren oder Comparator angeben
    - Kein null erlaubt

  Codebeispiel:
    import java.util.TreeSet;
    import java.util.Comparator;

    TreeSet<Integer> zahlen = new TreeSet<>();
    zahlen.add(5);
    zahlen.add(2);
    zahlen.add(8);
    // Automatisch sortiert: [2, 5, 8]

    Integer kleinstes = zahlen.first();   // 2
    Integer groesstes = zahlen.last();    // 8

    // Mit Comparator (absteigend)
    TreeSet<String> absteigend = new TreeSet<>(Comparator.reverseOrder());

  LINKEDHASHSET
  -------------
  Kombination aus HashSet und LinkedList. Behaelt Einfuegereihenfolge.

MAP - KEY-VALUE PAARE
=====================
Maps speichern Schluessel-Wert-Paare. Jeder Schluessel ist einzigartig.

  HASHMAP
  -------
  Die am haeufigsten verwendete Map-Implementierung.

  Eigenschaften:
    - put(), get(), remove(): O(1) durchschnittlich
    - Erlaubt einen null-Key und mehrere null-Values
    - Nicht synchronisiert

  Codebeispiel:
    import java.util.HashMap;
    import java.util.Map;

    public class HashMapDemo {
        public static void main(String[] args) {
            Map<String, Integer> alter = new HashMap<>();

            // Einfuegen
            alter.put("Alice", 30);
            alter.put("Bob", 25);
            alter.put("Charlie", 35);

            // Zugriff
            Integer aliceAlter = alter.get("Alice");  // 30
            Integer unbekannt = alter.get("Unbekannt");  // null

            // Sicherer Zugriff mit Default
            Integer sicher = alter.getOrDefault("Unbekannt", 0);

            // Pruefung
            boolean hatAlice = alter.containsKey("Alice");
            boolean hatAlter30 = alter.containsValue(30);

            // Iteration
            for (Map.Entry<String, Integer> entry : alter.entrySet()) {
                System.out.println(entry.getKey() + ": " + entry.getValue());
            }

            // Nur Keys oder Values
            for (String name : alter.keySet()) {
                System.out.println(name);
            }

            // Java 8+ Methoden
            alter.putIfAbsent("David", 28);
            alter.computeIfAbsent("Eva", k -> 22);
            alter.merge("Bob", 1, Integer::sum);  // Erhoeht Bobs Alter um 1
        }
    }

  TREEMAP
  -------
  Sortiert nach Schluesseln. Basiert auf Red-Black Tree.

    TreeMap<String, Integer> sortiert = new TreeMap<>();
    // Keys sind automatisch sortiert

  LINKEDHASHMAP
  -------------
  Behaelt Einfuegereihenfolge oder Zugriffsreihenfolge.

    // LRU-Cache mit maximal 100 Eintraegen
    Map<String, Object> cache = new LinkedHashMap<>(16, 0.75f, true) {
        @Override
        protected boolean removeEldestEntry(Map.Entry eldest) {
            return size() > 100;
        }
    };

STREAMS (JAVA 8+)
=================
Streams ermoeglichen funktionale Operationen auf Collections.

  Codebeispiel:
    import java.util.Arrays;
    import java.util.List;
    import java.util.stream.Collectors;

    public class StreamDemo {
        public static void main(String[] args) {
            List<Integer> zahlen = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

            // Filter und Map
            List<Integer> gerade = zahlen.stream()
                .filter(n -> n % 2 == 0)
                .map(n -> n * n)
                .collect(Collectors.toList());
            // Ergebnis: [4, 16, 36, 64, 100]

            // Reduce
            int summe = zahlen.stream()
                .reduce(0, Integer::sum);

            // Statistiken
            double durchschnitt = zahlen.stream()
                .mapToInt(Integer::intValue)
                .average()
                .orElse(0.0);

            // Gruppierung
            List<String> woerter = Arrays.asList("Apfel", "Birne", "Ananas");
            Map<Character, List<String>> gruppiert = woerter.stream()
                .collect(Collectors.groupingBy(s -> s.charAt(0)));

            // Parallel Streams (Vorsicht bei Seiteneffekten!)
            long count = zahlen.parallelStream()
                .filter(n -> n > 5)
                .count();
        }
    }

ITERATOREN UND FOREACH
======================
  // Enhanced for-loop (bevorzugt)
  for (String item : liste) {
      System.out.println(item);
  }

  // Iterator (wenn Entfernen noetig)
  Iterator<String> it = liste.iterator();
  while (it.hasNext()) {
      String item = it.next();
      if (item.startsWith("X")) {
          it.remove();  // Sicheres Entfernen waehrend Iteration
      }
  }

  // forEach mit Lambda (Java 8+)
  liste.forEach(item -> System.out.println(item));
  liste.forEach(System.out::println);

WICHTIGE UTILITY-METHODEN
=========================
Die Klasse Collections bietet nuetzliche statische Methoden:

  import java.util.Collections;

  // Sortieren
  Collections.sort(liste);
  Collections.sort(liste, Comparator.reverseOrder());

  // Suchen (Liste muss sortiert sein)
  int index = Collections.binarySearch(liste, "suchwort");

  // Umdrehen
  Collections.reverse(liste);

  // Mischen
  Collections.shuffle(liste);

  // Minimum/Maximum
  String min = Collections.min(liste);
  String max = Collections.max(liste);

  // Unmodifiable (Immutable Views)
  List<String> unveraenderlich = Collections.unmodifiableList(liste);

  // Synchronized Wrapper
  List<String> syncListe = Collections.synchronizedList(liste);

  // Leere Collections
  List<String> leer = Collections.emptyList();

BEST PRACTICES
==============
  1. Gegen Interfaces programmieren:
     List<String> list = new ArrayList<>();  // GUT
     ArrayList<String> list = new ArrayList<>();  // VERMEIDEN

  2. Initiale Kapazitaet angeben, wenn Groesse bekannt:
     List<Integer> liste = new ArrayList<>(10000);

  3. Richtige Implementierung waehlen:
     - Viel Lesen, wenig Schreiben: ArrayList
     - Viel Einfuegen/Loeschen: LinkedList
     - Einzigartigkeit wichtig: Set
     - Key-Value Zuordnung: Map

  4. Null-Handling beachten:
     - HashSet/HashMap erlauben null
     - TreeSet/TreeMap erlauben KEIN null

  5. equals() und hashCode() konsistent implementieren fuer eigene Klassen

  6. Streams fuer komplexe Transformationen nutzen

  7. ConcurrentHashMap statt synchronizedMap fuer Multithreading

HAEUFIGE FEHLER
===============
  - ConcurrentModificationException: Collection waehrend Iteration aendern
    Loesung: Iterator.remove() oder CopyOnWriteArrayList verwenden

  - Vergleich mit == statt equals() bei Wrapper-Objekten

  - Vergessen von hashCode() bei eigenen equals()-Implementierungen

SIEHE AUCH
==========
  wiki/java/generics/
  wiki/java/streams/
  wiki/java/multithreading/
  wiki/informatik/datenstrukturen/
  wiki/informatik/algorithmen/sortieren/
