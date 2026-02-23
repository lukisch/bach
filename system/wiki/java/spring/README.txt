# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: spring.io, docs.spring.io, Baeldung Spring Tutorials

SPRING FRAMEWORK
================

Stand: 2026-02-05

WAS IST SPRING?
---------------
Spring ist das fuehrende Java-Framework fuer Enterprise-Anwendungen.
Es bietet eine umfassende Infrastruktur fuer die Entwicklung von
Java-Applikationen mit Fokus auf Modularitaet und Testbarkeit.

Kernprinzipien:
  - Dependency Injection (DI) / Inversion of Control (IoC)
  - Aspektorientierte Programmierung (AOP)
  - Deklarative Transaktionsverwaltung
  - Convention over Configuration

SPRING BOOT
-----------
Spring Boot vereinfacht die Erstellung von Spring-Anwendungen:

  - Auto-Configuration: Automatische Konfiguration basierend auf Classpath
  - Embedded Server: Tomcat, Jetty oder Undertow integriert
  - Starter Dependencies: Vorkonfigurierte Dependency-Bundles
  - Production-Ready: Actuator fuer Monitoring und Health Checks

Minimale Spring Boot Anwendung:

  import org.springframework.boot.SpringApplication;
  import org.springframework.boot.autoconfigure.SpringBootApplication;

  @SpringBootApplication
  public class Application {
      public static void main(String[] args) {
          SpringApplication.run(Application.class, args);
      }
  }

DEPENDENCY INJECTION
--------------------
DI ist das Herzstueck von Spring. Container verwaltet Objekte (Beans):

  // 1. Constructor Injection (EMPFOHLEN)
  @Service
  public class UserService {
      private final UserRepository repository;

      public UserService(UserRepository repository) {
          this.repository = repository;
      }
  }

  // 2. Field Injection (VERMEIDEN)
  @Service
  public class UserService {
      @Autowired
      private UserRepository repository;  // Schwerer testbar
  }

  // 3. Setter Injection
  @Service
  public class UserService {
      private UserRepository repository;

      @Autowired
      public void setRepository(UserRepository repository) {
          this.repository = repository;
      }
  }

Bean-Annotationen:
  @Component    Generische Bean
  @Service      Business-Logik
  @Repository   Datenzugriff
  @Controller   Web-Controller
  @RestController  REST-API Controller

SPRING MVC
----------
Web-Framework fuer REST-APIs und Web-Anwendungen:

  @RestController
  @RequestMapping("/api/users")
  public class UserController {

      private final UserService userService;

      public UserController(UserService userService) {
          this.userService = userService;
      }

      @GetMapping
      public List<User> getAllUsers() {
          return userService.findAll();
      }

      @GetMapping("/{id}")
      public ResponseEntity<User> getUser(@PathVariable Long id) {
          return userService.findById(id)
              .map(ResponseEntity::ok)
              .orElse(ResponseEntity.notFound().build());
      }

      @PostMapping
      @ResponseStatus(HttpStatus.CREATED)
      public User createUser(@RequestBody @Valid UserDto dto) {
          return userService.create(dto);
      }

      @PutMapping("/{id}")
      public User updateUser(@PathVariable Long id,
                             @RequestBody @Valid UserDto dto) {
          return userService.update(id, dto);
      }

      @DeleteMapping("/{id}")
      @ResponseStatus(HttpStatus.NO_CONTENT)
      public void deleteUser(@PathVariable Long id) {
          userService.delete(id);
      }
  }

Request-Mapping Annotationen:
  @GetMapping       HTTP GET
  @PostMapping      HTTP POST
  @PutMapping       HTTP PUT
  @DeleteMapping    HTTP DELETE
  @PatchMapping     HTTP PATCH

SPRING DATA JPA
---------------
Vereinfacht Datenbankzugriff durch Repository-Abstraktionen:

  // Entity
  @Entity
  @Table(name = "users")
  public class User {
      @Id
      @GeneratedValue(strategy = GenerationType.IDENTITY)
      private Long id;

      @Column(nullable = false)
      private String username;

      @Column(unique = true)
      private String email;

      @OneToMany(mappedBy = "user", cascade = CascadeType.ALL)
      private List<Order> orders;

      // Getter, Setter, Konstruktoren
  }

  // Repository Interface
  public interface UserRepository extends JpaRepository<User, Long> {

      // Query Methods (automatisch implementiert)
      Optional<User> findByEmail(String email);
      List<User> findByUsernameContaining(String name);

      // Custom Query
      @Query("SELECT u FROM User u WHERE u.active = true")
      List<User> findAllActive();

      // Native Query
      @Query(value = "SELECT * FROM users WHERE created_at > ?1",
             nativeQuery = true)
      List<User> findRecentUsers(LocalDateTime since);
  }

SPRING SECURITY
---------------
Authentifizierung und Autorisierung:

  @Configuration
  @EnableWebSecurity
  public class SecurityConfig {

      @Bean
      public SecurityFilterChain filterChain(HttpSecurity http)
              throws Exception {
          http
              .csrf(csrf -> csrf.disable())
              .authorizeHttpRequests(auth -> auth
                  .requestMatchers("/api/public/**").permitAll()
                  .requestMatchers("/api/admin/**").hasRole("ADMIN")
                  .anyRequest().authenticated()
              )
              .sessionManagement(session -> session
                  .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
              )
              .oauth2ResourceServer(oauth2 -> oauth2
                  .jwt(Customizer.withDefaults())
              );
          return http.build();
      }

      @Bean
      public PasswordEncoder passwordEncoder() {
          return new BCryptPasswordEncoder();
      }
  }

KONFIGURATION
-------------
application.yml (oder application.properties):

  spring:
    application:
      name: myapp

    datasource:
      url: jdbc:postgresql://localhost:5432/mydb
      username: ${DB_USER}
      password: ${DB_PASSWORD}
      driver-class-name: org.postgresql.Driver

    jpa:
      hibernate:
        ddl-auto: validate
      show-sql: false
      properties:
        hibernate:
          format_sql: true

    profiles:
      active: ${SPRING_PROFILE:dev}

  server:
    port: 8080
    servlet:
      context-path: /api

Profile fuer verschiedene Umgebungen:
  application-dev.yml     Entwicklung
  application-test.yml    Tests
  application-prod.yml    Produktion

EXCEPTION HANDLING
------------------
Globale Fehlerbehandlung mit @ControllerAdvice:

  @RestControllerAdvice
  public class GlobalExceptionHandler {

      @ExceptionHandler(EntityNotFoundException.class)
      @ResponseStatus(HttpStatus.NOT_FOUND)
      public ErrorResponse handleNotFound(EntityNotFoundException ex) {
          return new ErrorResponse("NOT_FOUND", ex.getMessage());
      }

      @ExceptionHandler(MethodArgumentNotValidException.class)
      @ResponseStatus(HttpStatus.BAD_REQUEST)
      public ErrorResponse handleValidation(
              MethodArgumentNotValidException ex) {
          List<String> errors = ex.getBindingResult()
              .getFieldErrors()
              .stream()
              .map(e -> e.getField() + ": " + e.getDefaultMessage())
              .toList();
          return new ErrorResponse("VALIDATION_ERROR", errors);
      }

      @ExceptionHandler(Exception.class)
      @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
      public ErrorResponse handleGeneric(Exception ex) {
          log.error("Unhandled exception", ex);
          return new ErrorResponse("INTERNAL_ERROR",
              "Ein unerwarteter Fehler ist aufgetreten");
      }
  }

BEST PRACTICES
--------------
  1. Constructor Injection bevorzugen
     - Explizite Abhaengigkeiten
     - Immutable Felder (final)
     - Einfacher zu testen

  2. Profile fuer Umgebungen nutzen
     - Keine Secrets in Code
     - Umgebungsvariablen verwenden
     - Unterschiedliche Configs pro Umgebung

  3. DTOs von Entities trennen
     - API-Kontrakt von DB-Modell entkoppeln
     - Validierung auf DTO-Ebene
     - MapStruct fuer Mapping

  4. Layered Architecture
     - Controller -> Service -> Repository
     - Jede Schicht hat klare Verantwortung
     - Abhaengigkeiten nur nach unten

  5. Transaktionen richtig einsetzen
     - @Transactional auf Service-Methoden
     - Nur bei schreibenden Operationen
     - Rollback bei Exceptions

HAEUFIGE STARTER DEPENDENCIES
-----------------------------
  spring-boot-starter-web          REST APIs, MVC
  spring-boot-starter-data-jpa     JPA + Hibernate
  spring-boot-starter-security     Authentifizierung
  spring-boot-starter-validation   Bean Validation
  spring-boot-starter-actuator     Monitoring
  spring-boot-starter-test         Testing
  spring-boot-starter-cache        Caching
  spring-boot-starter-mail         E-Mail Versand

PROJEKTSTRUKTUR (EMPFOHLEN)
---------------------------
  src/main/java/com/example/myapp/
  +-- MyAppApplication.java
  +-- config/
  |   +-- SecurityConfig.java
  |   +-- DatabaseConfig.java
  +-- controller/
  |   +-- UserController.java
  +-- service/
  |   +-- UserService.java
  |   +-- impl/
  |       +-- UserServiceImpl.java
  +-- repository/
  |   +-- UserRepository.java
  +-- entity/
  |   +-- User.java
  +-- dto/
  |   +-- UserDto.java
  |   +-- CreateUserRequest.java
  +-- mapper/
  |   +-- UserMapper.java
  +-- exception/
      +-- GlobalExceptionHandler.java
      +-- EntityNotFoundException.java

SIEHE AUCH
==========
  wiki/java/README.txt           Java Uebersicht
  wiki/java/testing/README.txt   Testing mit JUnit, Mockito
  wiki/java/jdbc/README.txt      JDBC Grundlagen
  wiki/informatik/software_architektur/README.txt
