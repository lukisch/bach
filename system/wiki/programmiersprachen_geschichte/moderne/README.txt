================================================================================
PROGRAMMIERSPRACHEN: DIE MODERNE AERA (2000er bis heute)
================================================================================

+------------------------------------------------------------------------------+
| METADATEN                                                                    |
+------------------------------------------------------------------------------+
| Portabilitaet:     UNIVERSAL                                                 |
| Zuletzt validiert: 2026-02-05                                                |
| Naechste Pruefung: 2027-02-05                                                |
| Quellen:           TIOBE Index, Stack Overflow Developer Survey,             |
|                    GitHub Octoverse, offizielle Sprachdokumentationen,       |
|                    IEEE Spectrum Ranking                                     |
+------------------------------------------------------------------------------+

Stand: 2026-02-05
Status: VOLLSTAENDIGER ARTIKEL

================================================================================
EINFUEHRUNG
================================================================================

Die moderne Aera der Programmiersprachen ist gepraegt von fundamentalen
Veraenderungen in der Softwareentwicklung: Cloud Computing, Mobile Apps,
verteilte Systeme, Containerisierung und ein erneuter Fokus auf
Speichersicherheit und Nebenlaaufigkeit.

Im Gegensatz zu frueheren Jahrzehnten entstehen neue Sprachen nicht mehr
primaer in akademischen Umgebungen, sondern werden von grossen
Technologieunternehmen entwickelt, die spezifische Probleme loesen wollen:
Microsoft erschuf C# und TypeScript, Google entwickelte Go und Dart,
Apple fuehrte Swift ein, Mozilla schuf Rust, und JetBrains brachte Kotlin.

Die wichtigsten Trends dieser Aera:
  - Speichersicherheit ohne Laufzeit-Overhead
  - Native Unterstuetzung fuer Nebenlaeufigkeit
  - Null Safety als Sprachfeature
  - Moderne Typsysteme mit Type Inference
  - Interoperabilitaet mit bestehenden Oekosystemen

================================================================================
TEIL I: SPRACHEN DER 2000er JAHRE
================================================================================

C# (2000) - Microsofts Antwort auf Java
---------------------------------------

C# entstand als Teil von Microsofts .NET-Initiative und hat sich zu einer
der vielseitigsten Sprachen der Industrie entwickelt.

Entstehung:
  - Angekuendigt: 2000
  - Entwickler: Microsoft, Leitung Anders Hejlsberg
  - Hejlsberg: Zuvor Turbo Pascal und Delphi (Borland)
  - Motivation: Moderne Sprache fuer .NET Framework

Evolution der Sprache:
  C# 1.0 (2002) - Grundlegende OOP-Features, Delegates
  C# 2.0 (2005) - Generics, Nullable Types, Iteratoren
  C# 3.0 (2007) - LINQ, Lambda-Ausdruecke, var
  C# 4.0 (2010) - Dynamic Binding, optionale Parameter
  C# 5.0 (2012) - async/await revolutioniert Asynchronitaet
  C# 6.0 (2015) - Expression-bodied Members, Null-Propagation
  C# 7.x (2017) - Tuples, Pattern Matching, ref returns
  C# 8.0 (2019) - Nullable Reference Types, async streams
  C# 9.0 (2020) - Records, Init-only Properties
  C# 10.0 (2021) - Global Usings, File-scoped Namespaces
  C# 11.0 (2022) - Raw String Literals, List Patterns
  C# 12.0 (2023) - Collection Expressions, Primary Constructors
  C# 13.0 (2024) - Erweiterte Pattern Matching

Kernfeatures:
  +----------------------------------------------------------+
  |  // Async/Await - bahnbrechend fuer asynchronen Code     |
  |  public async Task<string> LadeAsync(string url)         |
  |  {                                                       |
  |      using var client = new HttpClient();                |
  |      return await client.GetStringAsync(url);            |
  |  }                                                       |
  |                                                          |
  |  // LINQ - deklarative Datenabfragen                     |
  |  var ergebnis = personen                                 |
  |      .Where(p => p.Alter >= 18)                          |
  |      .OrderBy(p => p.Name)                               |
  |      .Select(p => new { p.Name, p.Email });              |
  |                                                          |
  |  // Records - unveraenderliche Datentypen (C# 9+)        |
  |  public record Person(string Name, int Alter);           |
  +----------------------------------------------------------+

Einsatzgebiete:
  - Enterprise-Anwendungen (.NET)
  - Webentwicklung (ASP.NET Core)
  - Spieleentwicklung (Unity Engine - marktfuehrend)
  - Desktop-Anwendungen (WPF, WinForms, MAUI)
  - Cloud-Services (Azure)
  - Cross-Platform (.NET Core, .NET 5+)

Stand 2026:
  - .NET 9 aktuell, Cross-Platform Standard
  - Unity verwendet C# fuer Millionen von Spielen
  - Starke Position im Enterprise-Bereich
  - Aktive Weiterentwicklung mit jaehrlichen Releases

--------------------------------------------------------------------------------

SCALA (2004) - Funktional trifft Objektorientiert
-------------------------------------------------

Scala vereint objektorientierte und funktionale Programmierung auf der
Java Virtual Machine.

Entstehung:
  - Entwickler: Martin Odersky (EPFL, Schweiz)
  - Erste Version: 2004
  - Name: "Scalable Language"
  - Odersky: Mitarbeit an Java-Generics

Philosophie:
  - Jedes Programmierkonstrukt ist ein Objekt
  - Gleichzeitig vollstaendig funktional
  - Statisch typisiert mit Type Inference
  - Nahtlose Java-Interoperabilitaet
  - DSL-freundliche Syntax

Beispiel:
  +----------------------------------------------------------+
  |  // Case Classes - unveraenderliche Datenstrukturen      |
  |  case class Person(name: String, alter: Int)             |
  |                                                          |
  |  // Pattern Matching                                     |
  |  def beschreibe(x: Any): String = x match {              |
  |    case Person(n, a) if a >= 18 => s"$n ist erwachsen"   |
  |    case Person(n, _) => s"$n ist minderjaehrig"          |
  |    case _ => "Unbekannt"                                 |
  |  }                                                       |
  |                                                          |
  |  // Funktionale Transformation                           |
  |  val summe = (1 to 100).filter(_ % 2 == 0).sum           |
  +----------------------------------------------------------+

Frameworks:
  - Apache Spark (Big Data, geschrieben in Scala)
  - Play Framework (Web)
  - Akka (Actor-basierte Nebenlaeufigkeit)

Stand 2026:
  - Scala 3 (Dotty) brachte 2021 grosse Vereinfachungen
  - Starke Position im Big-Data-Bereich dank Spark
  - Nische, aber einflussreich

================================================================================
TEIL II: SPRACHEN DER 2010er JAHRE
================================================================================

GO (2009) - Googles Einfachheits-Revolution
-------------------------------------------

Go (auch Golang) wurde bei Google entwickelt, um die Komplexitaet moderner
Softwareentwicklung zu reduzieren und die Concurrency zu vereinfachen.

Entstehung:
  - Entwickler: Robert Griesemer, Rob Pike, Ken Thompson (Google)
  - Ken Thompson: Miterfinder von Unix und C
  - Rob Pike: Plan 9, UTF-8
  - Erste Veroeffentlichung: 2009

Designphilosophie:
  - "Less is more" - bewusster Verzicht auf Features
  - Schnelle Kompilierung (Sekunden, nicht Minuten)
  - Einfach zu lernen und zu lesen
  - Ein offensichtlicher Weg, Dinge zu tun
  - Eingebaute Werkzeuge (Format, Test, Docs)

Kernfeatures:
  +----------------------------------------------------------+
  |  // Goroutines - leichtgewichtige Threads                |
  |  func main() {                                           |
  |      go verarbeite(daten)  // Startet Goroutine          |
  |      go verarbeite(mehr)   // Tausende moeglich          |
  |  }                                                       |
  |                                                          |
  |  // Channels - sichere Kommunikation                     |
  |  func worker(jobs <-chan int, results chan<- int) {      |
  |      for j := range jobs {                               |
  |          results <- j * 2                                |
  |      }                                                   |
  |  }                                                       |
  |                                                          |
  |  // Interfaces - implizit erfuellt                       |
  |  type Stringer interface {                               |
  |      String() string                                     |
  |  }                                                       |
  |  // Jeder Typ mit String() Methode erfuellt Stringer     |
  |                                                          |
  |  // Error Handling - explizit, keine Exceptions          |
  |  f, err := os.Open("datei.txt")                          |
  |  if err != nil {                                         |
  |      return err                                          |
  |  }                                                       |
  +----------------------------------------------------------+

Was Go NICHT hat (bewusst):
  - Keine Generics (bis Go 1.18, 2022)
  - Keine Exceptions (explizite Fehlerbehandlung)
  - Keine Vererbung (Komposition stattdessen)
  - Kein Operator Overloading
  - Keine impliziten Konvertierungen

Einsatzgebiete:
  - Cloud-native Entwicklung (Docker, Kubernetes, Terraform)
  - Microservices und APIs
  - DevOps-Tools (Prometheus, Grafana, Vault)
  - Netzwerkprogrammierung
  - CLI-Tools

Stand 2026:
  - Go 1.22+ mit Generics vollstaendig etabliert
  - De-facto-Standard fuer Cloud-Infrastruktur
  - Konstant unter Top 10 im TIOBE Index

--------------------------------------------------------------------------------

RUST (2010) - Speichersicherheit ohne Kompromisse
-------------------------------------------------

Rust loest eines der schwierigsten Probleme der Systemprogrammierung:
Speichersicherheit ohne Garbage Collector.

Entstehung:
  - Begonnen: 2006 als persoenliches Projekt von Graydon Hoare
  - 2009: Mozilla uebernimmt das Projekt
  - 2010: Erste oeffentliche Ankuendigung
  - 2015: Rust 1.0 veroeffentlicht
  - 2021: Rust Foundation gegruendet (AWS, Google, Microsoft, Mozilla, Huawei)

Das Ownership-System:
  +----------------------------------------------------------+
  |  // Ownership - jeder Wert hat genau einen Owner         |
  |  let s1 = String::from("Hallo");                         |
  |  let s2 = s1;  // s1 ist jetzt UNGUELTIG (move)          |
  |                                                          |
  |  // Borrowing - temporaere Referenzen                    |
  |  fn laenge(s: &String) -> usize {  // Leiht nur          |
  |      s.len()                                             |
  |  }                                                       |
  |                                                          |
  |  // Mutable Borrowing - nur eine zur Zeit                |
  |  fn aendere(s: &mut String) {                            |
  |      s.push_str(" Welt");                                |
  |  }                                                       |
  +----------------------------------------------------------+

Borrow Checker - Kompilierzeit-Garantien:
  - Keine Null Pointer Dereferenzierungen
  - Keine Use-after-free Fehler
  - Keine Data Races bei Nebenlaeufigkeit
  - Keine Buffer Overflows
  - Keine Double Free

Result/Option statt Null/Exceptions:
  +----------------------------------------------------------+
  |  // Option fuer optionale Werte                          |
  |  fn finde(liste: &[i32], ziel: i32) -> Option<usize> {   |
  |      liste.iter().position(|&x| x == ziel)               |
  |  }                                                       |
  |                                                          |
  |  // Result fuer Fehlerbehandlung                         |
  |  fn lese_datei(pfad: &str) -> Result<String, io::Error> {|
  |      fs::read_to_string(pfad)                            |
  |  }                                                       |
  |                                                          |
  |  // Pattern Matching fuer Behandlung                     |
  |  match lese_datei("config.txt") {                        |
  |      Ok(inhalt) => println!("{}", inhalt),               |
  |      Err(e) => eprintln!("Fehler: {}", e),               |
  |  }                                                       |
  +----------------------------------------------------------+

Einsatzgebiete:
  - Systemprogrammierung (OS-Kernels, Treiber)
  - WebAssembly (fuehrende Sprache)
  - Kommandozeilen-Tools (ripgrep, fd, bat, exa)
  - Netzwerk-Services (Cloudflare, Discord)
  - Embedded Systems
  - Browser-Engines (Servo, Teile von Firefox)
  - Kryptographie und Sicherheit

Stand 2026:
  - "Most Loved Language" - Stack Overflow Survey (9 Jahre in Folge)
  - Linux Kernel akzeptiert Rust-Code (seit 2022)
  - Windows-Kernel integriert Rust (seit 2023)
  - Android nutzt Rust fuer sicherheitskritische Teile
  - Wachsende Adoption in Industrie und Forschung

--------------------------------------------------------------------------------

KOTLIN (2011) - Modernes Java
-----------------------------

Kotlin wurde von JetBrains entwickelt, um die Schwaechen von Java zu
beheben, waehrend volle Kompatibilitaet gewahrt bleibt.

Entstehung:
  - Entwickler: JetBrains (Hersteller von IntelliJ IDEA)
  - Erste Ankuendigung: 2011
  - Version 1.0: 2016
  - 2017: Google erklaert Kotlin zur bevorzugten Android-Sprache

Verbesserungen gegenueber Java:
  +----------------------------------------------------------+
  |  // Null Safety - in die Sprache eingebaut               |
  |  var name: String = "Hallo"     // Kann nicht null sein  |
  |  var nullable: String? = null   // Explizit nullable     |
  |  println(nullable?.length)      // Safe Call             |
  |  println(nullable ?: "default") // Elvis Operator        |
  |                                                          |
  |  // Data Classes (statt Java-Boilerplate)                |
  |  data class Person(val name: String, val alter: Int)     |
  |  // Generiert: equals, hashCode, toString, copy          |
  |                                                          |
  |  // Extension Functions                                  |
  |  fun String.verschluesselt(): String {                   |
  |      return this.reversed()  // Beispiel                 |
  |  }                                                       |
  |  "Hallo".verschluesselt()  // Aufruf                     |
  |                                                          |
  |  // Coroutines fuer Asynchronitaet                       |
  |  suspend fun ladeAsync(): Data {                         |
  |      return withContext(Dispatchers.IO) {                |
  |          api.fetch()                                     |
  |      }                                                   |
  |  }                                                       |
  +----------------------------------------------------------+

Einsatzgebiete:
  - Android-Entwicklung (de-facto Standard)
  - Server-side (Spring Boot, Ktor)
  - Multiplatform (iOS, Web, Desktop)
  - Build-Scripts (Gradle Kotlin DSL)

Stand 2026:
  - Kotlin 2.0+ mit K2 Compiler
  - Dominiert Android-Neuentwicklung
  - Kotlin Multiplatform zunehmend verbreitet

--------------------------------------------------------------------------------

TYPESCRIPT (2012) - JavaScript mit Typsystem
--------------------------------------------

TypeScript erweitert JavaScript um ein optionales statisches Typsystem
und ermoeglicht so Enterprise-taugliche Webentwicklung.

Entstehung:
  - Entwickler: Microsoft, Leitung Anders Hejlsberg
  - Erste Version: 2012
  - Motivation: Grosse JavaScript-Projekte wartbar machen

Kernkonzept:
  - Superset von JavaScript (jedes JS ist valides TS)
  - Kompiliert zu JavaScript
  - Typen sind optional und graduell einzufuehren
  - Exzellente Tooling-Unterstuetzung (IntelliSense)

Beispiel:
  +----------------------------------------------------------+
  |  // Interfaces definieren Strukturen                     |
  |  interface Benutzer {                                    |
  |      id: number;                                         |
  |      name: string;                                       |
  |      email?: string;  // Optional                        |
  |  }                                                       |
  |                                                          |
  |  // Generics                                             |
  |  function erster<T>(array: T[]): T | undefined {         |
  |      return array[0];                                    |
  |  }                                                       |
  |                                                          |
  |  // Union Types                                          |
  |  type Status = "aktiv" | "inaktiv" | "gesperrt";         |
  |                                                          |
  |  // Discriminated Unions fuer Zustandsmaschinen          |
  |  type Ergebnis<T> =                                      |
  |      | { success: true; data: T }                        |
  |      | { success: false; error: string };                |
  +----------------------------------------------------------+

Stand 2026:
  - De-facto Standard fuer professionelle Web-Entwicklung
  - Verwendet von: Angular, Vue 3, NestJS, Deno
  - React-Projekte ueberwiegend in TypeScript

--------------------------------------------------------------------------------

SWIFT (2014) - Apples moderne Sprache
-------------------------------------

Swift wurde als Nachfolger von Objective-C fuer das Apple-Oekosystem
entwickelt.

Entstehung:
  - Entwickler: Apple, Leitung Chris Lattner
  - Lattner: Zuvor LLVM und Clang
  - Angekuendigt: WWDC 2014
  - Open Source: 2015

Designziele:
  - Sicher (Null Safety, Bounds Checking)
  - Schnell (LLVM-optimiert, nahe an C)
  - Expressiv (moderne Syntax)
  - Interoperabel mit Objective-C

Beispiel:
  +----------------------------------------------------------+
  |  // Structs als Werttypen (bevorzugt)                    |
  |  struct Punkt {                                          |
  |      var x: Double                                       |
  |      var y: Double                                       |
  |                                                          |
  |      func distanz(zu: Punkt) -> Double {                 |
  |          let dx = x - zu.x                               |
  |          let dy = y - zu.y                               |
  |          return (dx*dx + dy*dy).squareRoot()             |
  |      }                                                   |
  |  }                                                       |
  |                                                          |
  |  // Optionals und Guard                                  |
  |  func verarbeite(text: String?) {                        |
  |      guard let sicher = text else {                      |
  |          print("Kein Text")                              |
  |          return                                          |
  |      }                                                   |
  |      print(sicher.uppercased())                          |
  |  }                                                       |
  +----------------------------------------------------------+

Stand 2026:
  - Obligatorisch fuer neue iOS/macOS-Entwicklung
  - Swift 6.0+ mit Actor-basierter Concurrency
  - Zunehmend server-side (Vapor Framework)
  - Swift for TensorFlow eingestellt, aber Einfluss auf ML-Bibliotheken

================================================================================
TEIL III: UEBERGREIFENDE TRENDS UND ENTWICKLUNGEN
================================================================================

SPEICHERSICHERHEIT
------------------
Der wichtigste Trend der 2020er: Speichersicherheit wird Prioritaet.

  Rust    -> Ownership-System, Compile-Zeit-Garantien
  Swift   -> ARC (Automatic Reference Counting), Optional Chaining
  Kotlin  -> Null Safety in der Sprache
  C#      -> Nullable Reference Types (opt-in ab C# 8)

Hintergrund: Microsoft und Google berichten, dass 70% aller
Sicherheitsluecken auf Speicherfehler zurueckgehen.

NULL SAFETY
-----------
"The Billion Dollar Mistake" (Tony Hoare ueber null) wird adressiert:

  Rust       -> Option<T> statt null
  Kotlin     -> Nullable Types (String?)
  Swift      -> Optionals
  TypeScript -> Strict Null Checks
  C#         -> Nullable Reference Types

NEBENLAEUFIKEIT (CONCURRENCY)
-----------------------------
Moderne Sprachen haben eingebaute Unterstuetzung:

  Go        -> Goroutines + Channels (CSP-Modell)
  Rust      -> async/await + Send/Sync Traits
  Kotlin    -> Coroutines
  Swift     -> Actors + structured concurrency
  C#        -> async/await (seit 2012, Vorreiter)

INTEROPERABILITAET
------------------
Neue Sprachen muessen mit bestehenden Oekosystemen arbeiten:

  Kotlin      -> 100% Java-kompatibel
  TypeScript  -> Kompiliert zu JavaScript
  Swift       -> Objective-C Bridging
  Rust        -> C FFI, wasm-bindgen

================================================================================
TEIL IV: ZUSAMMENFASSUNG
================================================================================

ZEITLEISTE MODERNER SPRACHEN
----------------------------
  2000 - C# angekuendigt (Microsoft)
  2004 - Scala 1.0 (Martin Odersky)
  2009 - Go angekuendigt (Google)
  2010 - Rust angekuendigt (Mozilla)
  2011 - Kotlin angekuendigt (JetBrains)
  2012 - TypeScript 0.8 (Microsoft)
  2014 - Swift angekuendigt (Apple)
  2015 - Rust 1.0
  2016 - Kotlin 1.0
  2017 - Kotlin wird offizielle Android-Sprache
  2021 - Rust Foundation gegruendet
  2022 - Go Generics (1.18), Rust im Linux Kernel

WICHTIGE PERSOENLICHKEITEN
--------------------------
  Anders Hejlsberg  - C#, TypeScript (zuvor Turbo Pascal, Delphi)
  Rob Pike          - Go (zuvor Plan 9, UTF-8)
  Ken Thompson      - Go (zuvor Unix, C, Plan 9)
  Graydon Hoare     - Rust (urspruenglicher Entwickler)
  Chris Lattner     - Swift (zuvor LLVM, Clang)
  Martin Odersky    - Scala

SPRACHEN NACH EINSATZGEBIET (Stand 2026)
----------------------------------------
  Cloud/DevOps:        Go, Rust
  Mobile (Android):    Kotlin
  Mobile (iOS):        Swift
  Web Frontend:        TypeScript
  Web Backend:         Go, Rust, Kotlin, TypeScript
  Enterprise:          C#, Kotlin, Java
  Systemprogrammierung: Rust, C, C++
  Spieleentwicklung:   C# (Unity), C++ (Unreal)
  Big Data:            Scala, Python

================================================================================
SIEHE AUCH
================================================================================

  wiki/programmiersprachen_geschichte/anfaenge/
  wiki/programmiersprachen_geschichte/strukturierte_aera/
  wiki/programmiersprachen_geschichte/oop_revolution/
  wiki/programmiersprachen_geschichte/zukunft/
  wiki/technologien/cloud_native/
  wiki/technologien/webassembly/
  wiki/konzepte/concurrency/

================================================================================
GEPLANTE VERTIEFENDE ARTIKEL
================================================================================

  [ ] rust_ownership.txt
  [ ] go_concurrency.txt
  [ ] kotlin_coroutines.txt
  [ ] typescript_typsystem.txt
  [ ] swift_memory_management.txt
  [ ] moderne_fehlerbehandlung.txt

================================================================================
                              Ende des Artikels
================================================================================
