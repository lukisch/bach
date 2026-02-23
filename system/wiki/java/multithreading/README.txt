JAVA MULTITHREADING
===================

# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05
# Naechste Pruefung: 2027-02-05
# Quellen: Oracle Java Documentation, Java Concurrency in Practice (Goetz)

Stand: 2026-02-05
Status: VOLLSTAENDIG

EINFUEHRUNG
===========
Multithreading ermoeglicht die gleichzeitige Ausfuehrung mehrerer
Programmteile innerhalb eines Prozesses. Java bietet von Grund auf
robuste Unterstuetzung fuer nebenlaeufige Programmierung durch:

  - Die Thread-Klasse und das Runnable-Interface
  - Synchronisationsmechanismen (synchronized, volatile)
  - Das java.util.concurrent Package (seit Java 5)
  - Das Fork/Join Framework (seit Java 7)
  - CompletableFuture (seit Java 8)
  - Virtual Threads (seit Java 21)

THREADS ERSTELLEN
=================
Es gibt mehrere Moeglichkeiten, Threads in Java zu erstellen:

  METHODE 1: THREAD KLASSE ERWEITERN
  ----------------------------------
  Codebeispiel:
    public class MeinThread extends Thread {

        private final String name;

        public MeinThread(String name) {
            this.name = name;
        }

        @Override
        public void run() {
            for (int i = 0; i < 5; i++) {
                System.out.println(name + ": Zaehler " + i);
                try {
                    Thread.sleep(100);  // 100ms pausieren
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return;
                }
            }
        }

        public static void main(String[] args) {
            MeinThread t1 = new MeinThread("Thread-A");
            MeinThread t2 = new MeinThread("Thread-B");

            t1.start();  // WICHTIG: start() nicht run()!
            t2.start();

            // Warten bis Threads fertig sind
            try {
                t1.join();
                t2.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }

            System.out.println("Alle Threads beendet");
        }
    }

  METHODE 2: RUNNABLE INTERFACE (EMPFOHLEN)
  -----------------------------------------
  Codebeispiel:
    public class RunnableDemo {
        public static void main(String[] args) {
            // Mit Klasse
            Runnable aufgabe = new MeineAufgabe();
            Thread t1 = new Thread(aufgabe);
            t1.start();

            // Mit Lambda (Java 8+) - bevorzugt
            Thread t2 = new Thread(() -> {
                System.out.println("Lambda-Thread laeuft");
            });
            t2.start();

            // Mit benanntem Thread
            Thread t3 = new Thread(() -> {
                System.out.println("Benannter Thread: " +
                    Thread.currentThread().getName());
            }, "MeinBenannterThread");
            t3.start();
        }
    }

    class MeineAufgabe implements Runnable {
        @Override
        public void run() {
            System.out.println("Aufgabe wird ausgefuehrt");
        }
    }

  VORTEILE VON RUNNABLE:
  - Klasse kann von anderer Klasse erben
  - Bessere Trennung von Aufgabe und Ausfuehrung
  - Kompatibel mit ExecutorService

THREAD LIFECYCLE
================
Ein Thread durchlaeuft verschiedene Zustaende:

  NEW           Thread erstellt, noch nicht gestartet
     |
     | start()
     v
  RUNNABLE      Bereit zur Ausfuehrung oder laeuft gerade
     |
     +-----------> BLOCKED     Wartet auf Monitor-Lock
     |                |
     |                | (Lock erhalten)
     |                v
     +-----------> WAITING     Wartet unbegrenzt (wait(), join())
     |                |
     |                | (notify(), join beendet)
     |                v
     +-----------> TIMED_WAITING  Wartet zeitbegrenzt (sleep(), wait(time))
     |                |
     |                | (Zeit abgelaufen, notify())
     |                v
     +<------------+
     |
     | run() beendet oder Exception
     v
  TERMINATED    Thread beendet

  THREAD-METHODEN:
    start()      - Startet den Thread
    run()        - Enthaelt die Ausfuehrungslogik (nicht direkt aufrufen!)
    sleep(ms)    - Pausiert den Thread
    join()       - Wartet auf Thread-Beendigung
    join(ms)     - Wartet maximal ms Millisekunden
    interrupt()  - Unterbricht wartenden Thread
    isAlive()    - Prueft ob Thread laeuft
    getName()    - Gibt Thread-Namen zurueck
    setName()    - Setzt Thread-Namen
    setPriority()- Setzt Thread-Prioritaet (1-10)

SYNCHRONISATION
===============
Synchronisation verhindert Race Conditions bei gleichzeitigem Zugriff
auf gemeinsame Ressourcen.

  SYNCHRONIZED METHODE
  --------------------
  Codebeispiel:
    public class Zaehler {
        private int wert = 0;

        // Nur ein Thread kann diese Methode gleichzeitig ausfuehren
        public synchronized void erhoehen() {
            wert++;
        }

        public synchronized int getWert() {
            return wert;
        }
    }

  SYNCHRONIZED BLOCK
  ------------------
  Codebeispiel:
    public class BankKonto {
        private double kontostand = 0;
        private final Object lock = new Object();

        public void einzahlen(double betrag) {
            synchronized (lock) {
                kontostand += betrag;
            }
        }

        public boolean abheben(double betrag) {
            synchronized (lock) {
                if (kontostand >= betrag) {
                    kontostand -= betrag;
                    return true;
                }
                return false;
            }
        }

        // Fuer static Methoden: synchronized auf Klasse
        public static synchronized void staticMethode() {
            // Lock auf BankKonto.class
        }
    }

  VOLATILE
  --------
  Garantiert Sichtbarkeit von Variablenaenderungen zwischen Threads:

  Codebeispiel:
    public class StoppbarerThread extends Thread {
        // Ohne volatile koennten Aenderungen unsichtbar sein
        private volatile boolean running = true;

        public void stoppen() {
            running = false;
        }

        @Override
        public void run() {
            while (running) {
                // Arbeit verrichten
                doWork();
            }
            System.out.println("Thread gestoppt");
        }
    }

  HINWEIS: volatile garantiert nur Sichtbarkeit, nicht Atomaritaet!
           Fuer atomare Operationen: AtomicInteger, AtomicLong, etc.

WAIT, NOTIFY, NOTIFYALL
=======================
Inter-Thread-Kommunikation mit Monitor-Objekten:

  Codebeispiel:
    public class ProducerConsumer {
        private final List<Integer> buffer = new ArrayList<>();
        private final int MAX_SIZE = 10;

        public synchronized void produce(int item) throws InterruptedException {
            while (buffer.size() == MAX_SIZE) {
                wait();  // Wartet und gibt Lock frei
            }
            buffer.add(item);
            System.out.println("Produziert: " + item);
            notifyAll();  // Weckt alle wartenden Threads
        }

        public synchronized int consume() throws InterruptedException {
            while (buffer.isEmpty()) {
                wait();
            }
            int item = buffer.remove(0);
            System.out.println("Konsumiert: " + item);
            notifyAll();
            return item;
        }
    }

  REGELN:
  - wait(), notify(), notifyAll() nur in synchronized Block aufrufen
  - Immer in while-Schleife warten (spurious wakeups)
  - notifyAll() ist sicherer als notify()

EXECUTOR SERVICE (JAVA 5+)
==========================
Modernes Thread-Pool-Management, bevorzugte Alternative zu direkter
Thread-Erstellung:

  Codebeispiel:
    import java.util.concurrent.*;

    public class ExecutorDemo {
        public static void main(String[] args) {
            // Fixed Thread Pool
            ExecutorService executor = Executors.newFixedThreadPool(4);

            // Aufgaben einreichen
            for (int i = 0; i < 10; i++) {
                final int taskNr = i;
                executor.submit(() -> {
                    System.out.println("Task " + taskNr + " auf " +
                        Thread.currentThread().getName());
                    return taskNr * 2;
                });
            }

            // Kein neuen Tasks mehr annehmen
            executor.shutdown();

            // Warten auf Beendigung
            try {
                if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                    executor.shutdownNow();
                }
            } catch (InterruptedException e) {
                executor.shutdownNow();
                Thread.currentThread().interrupt();
            }
        }
    }

  EXECUTOR-TYPEN:
    // Fester Thread-Pool
    ExecutorService fixed = Executors.newFixedThreadPool(4);

    // Dynamischer Pool (cachet Threads)
    ExecutorService cached = Executors.newCachedThreadPool();

    // Einzelner Thread (Aufgaben sequentiell)
    ExecutorService single = Executors.newSingleThreadExecutor();

    // Geplante Ausfuehrung
    ScheduledExecutorService scheduled = Executors.newScheduledThreadPool(2);
    scheduled.scheduleAtFixedRate(
        () -> System.out.println("Alle 5 Sekunden"),
        0, 5, TimeUnit.SECONDS);

FUTURE UND CALLABLE
===================
Fuer Aufgaben mit Rueckgabewert:

  Codebeispiel:
    import java.util.concurrent.*;

    public class FutureDemo {
        public static void main(String[] args) throws Exception {
            ExecutorService executor = Executors.newFixedThreadPool(2);

            // Callable hat Rueckgabewert (anders als Runnable)
            Callable<Integer> berechnung = () -> {
                Thread.sleep(2000);
                return 42;
            };

            // Future repraesentiert zukuenftiges Ergebnis
            Future<Integer> future = executor.submit(berechnung);

            // Andere Arbeit erledigen...
            System.out.println("Berechnung laeuft im Hintergrund...");

            // Ergebnis abholen (blockiert bis fertig)
            try {
                Integer ergebnis = future.get();  // Blockiert
                System.out.println("Ergebnis: " + ergebnis);

                // Mit Timeout
                Integer ergebnis2 = future.get(5, TimeUnit.SECONDS);

            } catch (TimeoutException e) {
                System.out.println("Timeout!");
                future.cancel(true);

            } catch (ExecutionException e) {
                System.out.println("Fehler in Task: " + e.getCause());
            }

            // Status pruefen
            boolean fertig = future.isDone();
            boolean abgebrochen = future.isCancelled();

            executor.shutdown();
        }
    }

COMPLETABLEFUTURE (JAVA 8+)
===========================
Moderne asynchrone Programmierung mit Fluent API:

  Codebeispiel:
    import java.util.concurrent.CompletableFuture;

    public class CompletableFutureDemo {
        public static void main(String[] args) {
            // Asynchrone Berechnung starten
            CompletableFuture<String> future = CompletableFuture
                .supplyAsync(() -> {
                    // Laeuft in ForkJoinPool.commonPool()
                    return fetchDatenVonServer();
                })
                .thenApply(daten -> {
                    // Transformation
                    return verarbeiteDaten(daten);
                })
                .thenApply(String::toUpperCase)
                .exceptionally(ex -> {
                    // Fehlerbehandlung
                    System.err.println("Fehler: " + ex.getMessage());
                    return "DEFAULT";
                });

            // Ergebnis abholen
            String ergebnis = future.join();
            System.out.println(ergebnis);

            // Mehrere Futures kombinieren
            CompletableFuture<String> f1 = CompletableFuture.supplyAsync(() -> "Hallo");
            CompletableFuture<String> f2 = CompletableFuture.supplyAsync(() -> "Welt");

            // Beide kombinieren
            CompletableFuture<String> kombiniert = f1.thenCombine(f2,
                (s1, s2) -> s1 + " " + s2);
            System.out.println(kombiniert.join());  // "Hallo Welt"

            // Auf alle warten
            CompletableFuture<Void> alle = CompletableFuture.allOf(f1, f2);
            alle.join();

            // Erstes Ergebnis nehmen
            CompletableFuture<Object> erstes = CompletableFuture.anyOf(f1, f2);
        }

        private static String fetchDatenVonServer() {
            return "Server-Daten";
        }

        private static String verarbeiteDaten(String daten) {
            return "Verarbeitet: " + daten;
        }
    }

CONCURRENT COLLECTIONS
======================
Thread-sichere Collection-Implementierungen:

  CONCURRENTHASHMAP
  -----------------
  Codebeispiel:
    import java.util.concurrent.ConcurrentHashMap;

    ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();

    // Atomare Operationen
    map.put("key", 1);
    map.putIfAbsent("key", 2);  // Nur wenn nicht vorhanden
    map.computeIfAbsent("key2", k -> berechneWert(k));
    map.merge("key", 1, Integer::sum);  // Addiert 1

    // Iteration ist thread-sicher (schwach konsistent)
    map.forEach((k, v) -> System.out.println(k + ": " + v));

  WEITERE CONCURRENT COLLECTIONS:
    CopyOnWriteArrayList   - Fuer seltene Writes, viele Reads
    CopyOnWriteArraySet    - Set-Version
    BlockingQueue          - Producer-Consumer Pattern
      - ArrayBlockingQueue
      - LinkedBlockingQueue
      - PriorityBlockingQueue
    ConcurrentLinkedQueue  - Non-blocking Queue
    ConcurrentSkipListMap  - Sortierte concurrent Map

  BLOCKINGQUEUE BEISPIEL:
    BlockingQueue<String> queue = new LinkedBlockingQueue<>(100);

    // Producer
    queue.put("item");      // Blockiert wenn voll
    queue.offer("item", 1, TimeUnit.SECONDS);  // Mit Timeout

    // Consumer
    String item = queue.take();  // Blockiert wenn leer
    String item2 = queue.poll(1, TimeUnit.SECONDS);  // Mit Timeout

LOCKS (JAVA.UTIL.CONCURRENT.LOCKS)
==================================
Erweiterte Lock-Mechanismen:

  REENTRANTLOCK
  -------------
  Codebeispiel:
    import java.util.concurrent.locks.*;

    public class LockDemo {
        private final ReentrantLock lock = new ReentrantLock();
        private int wert = 0;

        public void erhoehen() {
            lock.lock();
            try {
                wert++;
            } finally {
                lock.unlock();  // IMMER in finally!
            }
        }

        public void versucheErhoehen() {
            // Versucht Lock zu bekommen
            if (lock.tryLock()) {
                try {
                    wert++;
                } finally {
                    lock.unlock();
                }
            } else {
                System.out.println("Lock nicht verfuegbar");
            }
        }
    }

  READWRITELOCK
  -------------
  Mehrere Leser gleichzeitig, aber nur ein Schreiber:

    ReadWriteLock rwLock = new ReentrantReadWriteLock();

    // Lesen (mehrere gleichzeitig)
    rwLock.readLock().lock();
    try {
        return daten.get(key);
    } finally {
        rwLock.readLock().unlock();
    }

    // Schreiben (exklusiv)
    rwLock.writeLock().lock();
    try {
        daten.put(key, value);
    } finally {
        rwLock.writeLock().unlock();
    }

ATOMIC KLASSEN
==============
Lock-freie atomare Operationen:

  Codebeispiel:
    import java.util.concurrent.atomic.*;

    AtomicInteger zaehler = new AtomicInteger(0);

    zaehler.incrementAndGet();     // ++zaehler
    zaehler.getAndIncrement();     // zaehler++
    zaehler.addAndGet(5);          // zaehler += 5
    zaehler.compareAndSet(5, 10);  // Wenn 5, setze auf 10

    // AtomicReference fuer Objekte
    AtomicReference<String> ref = new AtomicReference<>("initial");
    ref.compareAndSet("initial", "updated");

VIRTUAL THREADS (JAVA 21+)
==========================
Leichtgewichtige Threads fuer hohe Nebenlaeufigkeit:

  Codebeispiel:
    // Virtual Thread erstellen
    Thread vThread = Thread.ofVirtual()
        .name("mein-virtual-thread")
        .start(() -> {
            System.out.println("Virtual Thread laeuft");
        });

    // Virtual Thread Executor
    try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
        for (int i = 0; i < 10000; i++) {
            executor.submit(() -> {
                // Jede Aufgabe bekommt eigenen Virtual Thread
                Thread.sleep(1000);
                return "fertig";
            });
        }
    }  // Auto-shutdown

  VORTEILE:
  - Sehr geringer Speicherverbrauch
  - Millionen von Threads moeglich
  - Blocking I/O wird automatisch optimiert

BEST PRACTICES
==============
  1. IMMUTABILITY BEVORZUGEN
     Unveraenderliche Objekte sind automatisch thread-sicher

  2. THREAD-SICHERE KLASSEN VERWENDEN
     ConcurrentHashMap statt synchronized HashMap

  3. EXECUTOR SERVICE NUTZEN
     Nicht manuell Threads erstellen und verwalten

  4. DEADLOCKS VERMEIDEN
     - Locks immer in gleicher Reihenfolge holen
     - tryLock() mit Timeout verwenden
     - So wenig wie moeglich locken

  5. RACE CONDITIONS ERKENNEN
     check-then-act Muster atomar machen

  6. INTERRUPTED EXCEPTION BEHANDELN
     Thread.currentThread().interrupt() aufrufen

  7. FINALLY FUER UNLOCK
     lock.unlock() immer in finally-Block

  8. VIRTUAL THREADS (JAVA 21+)
     Fuer I/O-lastige Aufgaben bevorzugen

HAEUFIGE PROBLEME
=================
  DEADLOCK
    Thread A wartet auf Lock von B, B wartet auf Lock von A

  LIVELOCK
    Threads reagieren aufeinander, kommen aber nicht voran

  STARVATION
    Ein Thread bekommt nie CPU-Zeit

  RACE CONDITION
    Ergebnis haengt von Thread-Reihenfolge ab

SIEHE AUCH
==========
  wiki/java/collections/
  wiki/java/streams/
  wiki/java/exceptions/
  wiki/patterns/producer_consumer/
  wiki/patterns/singleton/
  wiki/python/multithreading/
