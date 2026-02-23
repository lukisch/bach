# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: docs.python.org/3/library/threading.html,
#          docs.python.org/3/library/asyncio.html,
#          Real Python, Python Concurrency Cookbook

MULTITHREADING IN PYTHON
========================

Stand: 2026-02-05

UEBERBLICK
==========
  Python bietet mehrere Ansaetze fuer parallele Ausfuehrung:

  Threading:       Mehrere Threads, geteilter Speicher
  Multiprocessing: Mehrere Prozesse, separater Speicher
  Asyncio:         Kooperatives Multitasking, ein Thread

  Wichtig: Der GIL (Global Interpreter Lock) limitiert
  CPU-bound Threading in CPython.

GIL (GLOBAL INTERPRETER LOCK)
=============================

WAS IST DER GIL?
----------------
  - Mutex der CPython-Interpreter schuetzt
  - Nur ein Thread kann Python-Bytecode ausfuehren
  - Verhindert echte Parallelitaet bei CPU-Aufgaben
  - I/O-Operationen geben GIL frei

WANN IST DER GIL EIN PROBLEM?
-----------------------------
  CPU-bound:  Berechnung, Kompression, Parsing
              -> GIL limitiert, Multiprocessing nutzen

  I/O-bound:  Netzwerk, Dateien, Datenbank
              -> GIL kein Problem, Threading funktioniert

THREADING MODUL
===============

GRUNDLAGEN
----------
  import threading
  import time

  def aufgabe(name, dauer):
      print(f"{name} startet")
      time.sleep(dauer)
      print(f"{name} fertig")

  # Thread erstellen und starten
  thread = threading.Thread(target=aufgabe, args=("Task1", 2))
  thread.start()

  # Auf Thread warten
  thread.join()
  print("Alles fertig")

MEHRERE THREADS
---------------
  def download_datei(url):
      print(f"Download: {url}")
      time.sleep(1)  # Simuliert Download
      return f"Inhalt von {url}"

  urls = ["url1.com", "url2.com", "url3.com"]
  threads = []

  # Threads starten
  for url in urls:
      t = threading.Thread(target=download_datei, args=(url,))
      threads.append(t)
      t.start()

  # Auf alle warten
  for t in threads:
      t.join()

THREAD MIT RUECKGABEWERT
------------------------
  import threading

  class ThreadMitErgebnis(threading.Thread):
      def __init__(self, func, args=()):
          super().__init__()
          self.func = func
          self.args = args
          self.result = None

      def run(self):
          self.result = self.func(*self.args)

  def berechne(x):
      return x * x

  thread = ThreadMitErgebnis(berechne, (5,))
  thread.start()
  thread.join()
  print(thread.result)  # 25

THREAD SYNCHRONISATION
======================

LOCK (MUTEX)
------------
  import threading

  zaehler = 0
  lock = threading.Lock()

  def erhoehe_zaehler():
      global zaehler
      for _ in range(100000):
          with lock:  # Thread-sicher
              zaehler += 1

  threads = [threading.Thread(target=erhoehe_zaehler) for _ in range(5)]
  for t in threads:
      t.start()
  for t in threads:
      t.join()

  print(zaehler)  # Exakt 500000

RLOCK (REENTRANT LOCK)
----------------------
  # Kann mehrfach vom selben Thread acquired werden

  rlock = threading.RLock()

  def rekursive_funktion(n):
      with rlock:
          if n > 0:
              print(n)
              rekursive_funktion(n - 1)

SEMAPHORE
---------
  # Begrenzt gleichzeitige Zugriffe

  max_verbindungen = threading.Semaphore(3)

  def zugriff_auf_ressource(name):
      with max_verbindungen:
          print(f"{name} hat Zugriff")
          time.sleep(1)
          print(f"{name} fertig")

  # Nur 3 Threads gleichzeitig

EVENT
-----
  # Signalisierung zwischen Threads

  daten_bereit = threading.Event()

  def produzent():
      print("Produziere Daten...")
      time.sleep(2)
      daten_bereit.set()  # Signal senden

  def konsument():
      print("Warte auf Daten...")
      daten_bereit.wait()  # Blockiert bis set()
      print("Daten erhalten!")

  threading.Thread(target=produzent).start()
  threading.Thread(target=konsument).start()

CONDITION
---------
  # Komplexere Koordination

  condition = threading.Condition()
  queue = []

  def produzent():
      for i in range(5):
          with condition:
              queue.append(i)
              condition.notify()  # Konsument wecken
          time.sleep(0.5)

  def konsument():
      while True:
          with condition:
              while not queue:
                  condition.wait()  # Warten auf notify
              item = queue.pop(0)
              print(f"Verarbeitet: {item}")

CONCURRENT.FUTURES
==================

THREADPOOLEXECUTOR
------------------
  from concurrent.futures import ThreadPoolExecutor, as_completed

  def lade_url(url):
      import urllib.request
      with urllib.request.urlopen(url) as response:
          return len(response.read())

  urls = [
      'https://python.org',
      'https://github.com',
      'https://wikipedia.org'
  ]

  # Mit Context Manager (empfohlen):
  with ThreadPoolExecutor(max_workers=3) as executor:
      # map() fuer einfache Faelle:
      ergebnisse = list(executor.map(lade_url, urls))

      # submit() fuer mehr Kontrolle:
      futures = {executor.submit(lade_url, url): url for url in urls}

      for future in as_completed(futures):
          url = futures[future]
          try:
              groesse = future.result()
              print(f"{url}: {groesse} bytes")
          except Exception as e:
              print(f"{url} fehlgeschlagen: {e}")

PROCESSPOOLEXECUTOR
-------------------
  from concurrent.futures import ProcessPoolExecutor

  def cpu_intensive(n):
      """CPU-bound Aufgabe."""
      return sum(i * i for i in range(n))

  if __name__ == '__main__':  # Wichtig fuer Windows!
      zahlen = [10**6, 10**6, 10**6, 10**6]

      with ProcessPoolExecutor(max_workers=4) as executor:
          ergebnisse = list(executor.map(cpu_intensive, zahlen))

      print(ergebnisse)

MULTIPROCESSING MODUL
=====================

GRUNDLAGEN
----------
  from multiprocessing import Process, Value, Array

  def aufgabe(name):
      print(f"Prozess {name} mit PID {os.getpid()}")

  if __name__ == '__main__':
      prozesse = []
      for i in range(4):
          p = Process(target=aufgabe, args=(f"Worker-{i}",))
          prozesse.append(p)
          p.start()

      for p in prozesse:
          p.join()

GETEILTER SPEICHER
------------------
  from multiprocessing import Process, Value, Lock

  def erhoehen(zaehler, lock):
      for _ in range(10000):
          with lock:
              zaehler.value += 1

  if __name__ == '__main__':
      zaehler = Value('i', 0)  # 'i' = integer
      lock = Lock()

      prozesse = [Process(target=erhoehen, args=(zaehler, lock))
                  for _ in range(4)]

      for p in prozesse:
          p.start()
      for p in prozesse:
          p.join()

      print(zaehler.value)  # 40000

QUEUE FUER KOMMUNIKATION
------------------------
  from multiprocessing import Process, Queue

  def produzent(queue):
      for i in range(5):
          queue.put(f"Item {i}")

  def konsument(queue):
      while True:
          item = queue.get()
          if item is None:  # Poison Pill
              break
          print(f"Verarbeitet: {item}")

  if __name__ == '__main__':
      queue = Queue()

      p = Process(target=produzent, args=(queue,))
      c = Process(target=konsument, args=(queue,))

      p.start()
      c.start()

      p.join()
      queue.put(None)  # Signal zum Beenden
      c.join()

POOL
----
  from multiprocessing import Pool

  def quadrat(x):
      return x * x

  if __name__ == '__main__':
      with Pool(processes=4) as pool:
          # map() - gleiche Reihenfolge
          ergebnisse = pool.map(quadrat, range(10))

          # imap() - Iterator, spart Speicher
          for e in pool.imap(quadrat, range(10)):
              print(e)

          # apply_async() - einzelne Aufgabe
          result = pool.apply_async(quadrat, (5,))
          print(result.get())  # 25

ASYNCIO (ASYNCHRONE PROGRAMMIERUNG)
===================================

GRUNDLAGEN
----------
  import asyncio

  async def aufgabe(name, dauer):
      print(f"{name} startet")
      await asyncio.sleep(dauer)  # Non-blocking!
      print(f"{name} fertig")
      return f"Ergebnis von {name}"

  async def main():
      # Sequenziell (langsam):
      await aufgabe("A", 1)
      await aufgabe("B", 1)

      # Parallel (schnell):
      ergebnisse = await asyncio.gather(
          aufgabe("A", 1),
          aufgabe("B", 1)
      )
      print(ergebnisse)

  # Ausfuehren:
  asyncio.run(main())

MEHRERE TASKS
-------------
  async def download(url):
      print(f"Starte Download: {url}")
      await asyncio.sleep(1)  # Simuliert I/O
      return f"Inhalt von {url}"

  async def main():
      urls = ["url1.com", "url2.com", "url3.com"]

      # Alle parallel starten:
      tasks = [asyncio.create_task(download(url)) for url in urls]

      # Auf alle warten:
      ergebnisse = await asyncio.gather(*tasks)

      # Oder mit as_completed:
      for coro in asyncio.as_completed(tasks):
          ergebnis = await coro
          print(f"Fertig: {ergebnis}")

ASYNC CONTEXT MANAGER
---------------------
  import aiohttp

  async def fetch_url(session, url):
      async with session.get(url) as response:
          return await response.text()

  async def main():
      async with aiohttp.ClientSession() as session:
          html = await fetch_url(session, "https://python.org")
          print(len(html))

  asyncio.run(main())

ASYNC GENERATOR
---------------
  async def async_range(start, stop):
      for i in range(start, stop):
          await asyncio.sleep(0.1)
          yield i

  async def main():
      async for num in async_range(0, 5):
          print(num)

WANN WAS VERWENDEN?
===================

ENTSCHEIDUNGSBAUM
-----------------
  I/O-bound (Netzwerk, Dateien)?
  |
  +-- Ja --> Viele gleichzeitige Verbindungen?
  |          |
  |          +-- Ja --> asyncio (aiohttp, asyncpg)
  |          +-- Nein -> Threading oder asyncio
  |
  +-- Nein -> CPU-bound (Berechnung)?
              |
              +-- Ja --> multiprocessing / ProcessPoolExecutor
              +-- Nein -> Normaler Code reicht

UEBERSICHT
----------
  | Aufgabe            | Empfehlung              |
  |--------------------|-------------------------|
  | HTTP Requests      | asyncio + aiohttp       |
  | Datei-Downloads    | ThreadPoolExecutor      |
  | Datenverarbeitung  | ProcessPoolExecutor     |
  | GUI + Background   | Threading               |
  | Web Scraping       | asyncio + aiohttp       |
  | Wissenschaft       | multiprocessing + numpy |

BEST PRACTICES
==============

THREADING
---------
  - Immer with lock: statt lock.acquire()/release()
  - Daemon Threads fuer Hintergrundaufgaben
  - ThreadPoolExecutor statt manuelle Thread-Verwaltung
  - Vermeiden: Globale Variablen ohne Lock

MULTIPROCESSING
---------------
  - Immer if __name__ == '__main__': (Windows!)
  - Pool fuer viele gleiche Aufgaben
  - Queue fuer Kommunikation
  - Grosse Daten: SharedMemory statt Queue

ASYNCIO
-------
  - asyncio.run() fuer Einstiegspunkt
  - await nicht vergessen!
  - aiohttp statt requests
  - asyncpg statt psycopg2

DEBUGGING TIPPS
===============

THREAD-PROBLEME FINDEN
----------------------
  import threading
  import sys

  # Alle aktiven Threads anzeigen:
  for thread in threading.enumerate():
      print(f"{thread.name}: {thread.is_alive()}")

  # Stack Trace aller Threads:
  for thread_id, frame in sys._current_frames().items():
      print(f"\nThread {thread_id}:")
      import traceback
      traceback.print_stack(frame)

DEADLOCK VERMEIDEN
------------------
  - Locks immer in gleicher Reihenfolge acquiren
  - Timeouts verwenden: lock.acquire(timeout=5)
  - Context Manager nutzen
  - Lock-Hierarchien dokumentieren

RACE CONDITIONS
---------------
  # Schlecht:
  if zaehler > 0:
      zaehler -= 1  # Nicht atomar!

  # Gut:
  with lock:
      if zaehler > 0:
          zaehler -= 1

BACH-INTEGRATION
================
  Partner-Zuweisung:
    - Claude: Architekturentscheidung, Code-Review
    - Ollama: Lokale parallele Verarbeitung

  Typische Anwendungen:
    - Parallele API-Abfragen (asyncio)
    - Batch-Verarbeitung (ProcessPoolExecutor)
    - Hintergrund-Tasks in GUIs (Threading)

BEISPIEL: PARALLELER WEB-SCRAPER
================================
  import asyncio
  import aiohttp
  from typing import List, Dict

  async def fetch_page(session: aiohttp.ClientSession,
                       url: str) -> Dict:
      try:
          async with session.get(url, timeout=10) as response:
              text = await response.text()
              return {"url": url, "status": response.status,
                      "length": len(text)}
      except Exception as e:
          return {"url": url, "error": str(e)}

  async def scrape_all(urls: List[str]) -> List[Dict]:
      async with aiohttp.ClientSession() as session:
          tasks = [fetch_page(session, url) for url in urls]
          return await asyncio.gather(*tasks)

  if __name__ == '__main__':
      urls = ["https://python.org", "https://github.com"]
      results = asyncio.run(scrape_all(urls))
      for r in results:
          print(r)

SIEHE AUCH
==========
  wiki/python/best_practices/      Python Best Practices
  wiki/python/api/                 API-Entwicklung
  wiki/automatisierung/            Automatisierung allgemein
  wiki/informatik/programmierung/  Programmierkonzepte
