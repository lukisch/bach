# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: junit.org, site.mockito.org, Baeldung Testing Tutorials

JAVA TESTING - JUNIT UND MOCKITO
================================

Stand: 2026-02-05

UEBERBLICK
----------
Testing ist essenziell fuer zuverlaessige Software. Java bietet
ein ausgereiftes Testing-Oekosystem mit JUnit als Test-Framework
und Mockito fuer Mocking.

Testarten:
  Unit Tests         Einzelne Klassen isoliert testen
  Integration Tests  Zusammenspiel mehrerer Komponenten
  End-to-End Tests   Gesamte Anwendung von aussen

JUNIT 5 (JUPITER)
-----------------
JUnit 5 ist der aktuelle Standard fuer Java-Tests.

Grundstruktur eines Tests:

  import org.junit.jupiter.api.*;
  import static org.junit.jupiter.api.Assertions.*;

  class CalculatorTest {

      private Calculator calculator;

      @BeforeEach
      void setUp() {
          calculator = new Calculator();
      }

      @Test
      @DisplayName("Addition zweier positiver Zahlen")
      void addTwoPositiveNumbers() {
          // Arrange
          int a = 5;
          int b = 3;

          // Act
          int result = calculator.add(a, b);

          // Assert
          assertEquals(8, result);
      }

      @Test
      void divisionByZeroThrowsException() {
          assertThrows(ArithmeticException.class, () -> {
              calculator.divide(10, 0);
          });
      }

      @AfterEach
      void tearDown() {
          // Aufraeumen nach jedem Test
      }
  }

LIFECYCLE ANNOTATIONEN
----------------------
  @BeforeAll     Einmal vor allen Tests (static)
  @AfterAll      Einmal nach allen Tests (static)
  @BeforeEach    Vor jedem einzelnen Test
  @AfterEach     Nach jedem einzelnen Test
  @Test          Markiert eine Test-Methode
  @Disabled      Test temporaer deaktivieren
  @DisplayName   Lesbarer Test-Name

ASSERTIONS
----------
JUnit 5 bietet umfangreiche Assertions:

  // Gleichheit
  assertEquals(expected, actual);
  assertEquals(expected, actual, "Fehlermeldung");
  assertNotEquals(unexpected, actual);

  // Boolean
  assertTrue(condition);
  assertFalse(condition);

  // Null-Checks
  assertNull(object);
  assertNotNull(object);

  // Referenz-Gleichheit
  assertSame(expected, actual);
  assertNotSame(unexpected, actual);

  // Arrays
  assertArrayEquals(expectedArray, actualArray);

  // Iterables
  assertIterableEquals(expectedList, actualList);

  // Exceptions
  Exception ex = assertThrows(IllegalArgumentException.class, () -> {
      service.process(null);
  });
  assertEquals("Input darf nicht null sein", ex.getMessage());

  // Keine Exception
  assertDoesNotThrow(() -> service.process("valid"));

  // Alle Assertions ausfuehren (auch bei Fehler)
  assertAll("User Validierung",
      () -> assertEquals("Max", user.getFirstName()),
      () -> assertEquals("Mustermann", user.getLastName()),
      () -> assertNotNull(user.getEmail())
  );

  // Timeout
  assertTimeout(Duration.ofSeconds(2), () -> {
      slowService.execute();
  });

PARAMETRISIERTE TESTS
---------------------
Tests mit verschiedenen Eingabedaten wiederholen:

  import org.junit.jupiter.params.ParameterizedTest;
  import org.junit.jupiter.params.provider.*;

  class MathUtilsTest {

      @ParameterizedTest
      @ValueSource(ints = {2, 4, 6, 8, 100})
      void isEven_shouldReturnTrue(int number) {
          assertTrue(MathUtils.isEven(number));
      }

      @ParameterizedTest
      @NullAndEmptySource
      @ValueSource(strings = {"  ", "\t", "\n"})
      void isBlank_shouldReturnTrue(String input) {
          assertTrue(StringUtils.isBlank(input));
      }

      @ParameterizedTest
      @CsvSource({
          "1, 1, 2",
          "2, 3, 5",
          "10, 20, 30",
          "-5, 5, 0"
      })
      void add_shouldReturnSum(int a, int b, int expected) {
          assertEquals(expected, calculator.add(a, b));
      }

      @ParameterizedTest
      @MethodSource("provideStringsForLength")
      void stringLength_shouldBeCorrect(String input, int expected) {
          assertEquals(expected, input.length());
      }

      static Stream<Arguments> provideStringsForLength() {
          return Stream.of(
              Arguments.of("hello", 5),
              Arguments.of("", 0),
              Arguments.of("Java", 4)
          );
      }
  }

MOCKITO GRUNDLAGEN
------------------
Mockito erstellt Test-Doubles fuer Abhaengigkeiten:

  import org.mockito.Mock;
  import org.mockito.InjectMocks;
  import org.mockito.junit.jupiter.MockitoExtension;
  import static org.mockito.Mockito.*;

  @ExtendWith(MockitoExtension.class)
  class UserServiceTest {

      @Mock
      private UserRepository userRepository;

      @Mock
      private EmailService emailService;

      @InjectMocks
      private UserService userService;

      @Test
      void findById_shouldReturnUser() {
          // Arrange - Verhalten definieren
          User mockUser = new User(1L, "Max", "max@test.de");
          when(userRepository.findById(1L))
              .thenReturn(Optional.of(mockUser));

          // Act
          Optional<User> result = userService.findById(1L);

          // Assert
          assertTrue(result.isPresent());
          assertEquals("Max", result.get().getName());

          // Verify - Wurde Methode aufgerufen?
          verify(userRepository).findById(1L);
          verify(emailService, never()).sendEmail(any());
      }
  }

STUBBING (VERHALTEN DEFINIEREN)
-------------------------------
  // Rueckgabewert definieren
  when(mock.method()).thenReturn(value);

  // Mehrere Aufrufe, verschiedene Werte
  when(mock.method())
      .thenReturn(firstValue)
      .thenReturn(secondValue)
      .thenThrow(new RuntimeException());

  // Exception werfen
  when(mock.method()).thenThrow(new IllegalStateException());

  // Void-Methoden
  doNothing().when(mock).voidMethod();
  doThrow(new RuntimeException()).when(mock).voidMethod();

  // Argument Matchers
  when(repository.findByName(anyString())).thenReturn(user);
  when(repository.findById(eq(1L))).thenReturn(Optional.of(user));
  when(service.process(any(Request.class))).thenReturn(response);

  // Answer fuer dynamisches Verhalten
  when(repository.save(any(User.class)))
      .thenAnswer(invocation -> {
          User user = invocation.getArgument(0);
          user.setId(1L);
          return user;
      });

VERIFICATION (AUFRUFE PRUEFEN)
------------------------------
  // Genau einmal aufgerufen
  verify(mock).method();
  verify(mock, times(1)).method();

  // Mehrfach aufgerufen
  verify(mock, times(3)).method();
  verify(mock, atLeast(2)).method();
  verify(mock, atMost(5)).method();
  verify(mock, atLeastOnce()).method();

  // Nie aufgerufen
  verify(mock, never()).method();

  // Keine weiteren Interaktionen
  verifyNoMoreInteractions(mock);
  verifyNoInteractions(otherMock);

  // Reihenfolge pruefen
  InOrder inOrder = inOrder(mock1, mock2);
  inOrder.verify(mock1).firstMethod();
  inOrder.verify(mock2).secondMethod();

  // Argument Captor
  ArgumentCaptor<User> captor = ArgumentCaptor.forClass(User.class);
  verify(repository).save(captor.capture());
  User savedUser = captor.getValue();
  assertEquals("Max", savedUser.getName());

SPRING BOOT TESTING
-------------------
Spring Boot bietet spezielle Test-Annotationen:

  // Vollstaendiger Integrationstest
  @SpringBootTest
  class ApplicationIntegrationTest {

      @Autowired
      private UserService userService;

      @Test
      void contextLoads() {
          assertNotNull(userService);
      }
  }

  // Web Layer Test (nur Controller)
  @WebMvcTest(UserController.class)
  class UserControllerTest {

      @Autowired
      private MockMvc mockMvc;

      @MockBean
      private UserService userService;

      @Test
      void getUser_shouldReturnUser() throws Exception {
          User user = new User(1L, "Max", "max@test.de");
          when(userService.findById(1L)).thenReturn(Optional.of(user));

          mockMvc.perform(get("/api/users/1"))
              .andExpect(status().isOk())
              .andExpect(jsonPath("$.name").value("Max"))
              .andExpect(jsonPath("$.email").value("max@test.de"));
      }

      @Test
      void getUser_shouldReturn404_whenNotFound() throws Exception {
          when(userService.findById(99L)).thenReturn(Optional.empty());

          mockMvc.perform(get("/api/users/99"))
              .andExpect(status().isNotFound());
      }

      @Test
      void createUser_shouldCreateAndReturn201() throws Exception {
          String json = """
              {
                  "name": "Max",
                  "email": "max@test.de"
              }
              """;

          mockMvc.perform(post("/api/users")
                  .contentType(MediaType.APPLICATION_JSON)
                  .content(json))
              .andExpect(status().isCreated());
      }
  }

  // Repository Test (mit H2 In-Memory DB)
  @DataJpaTest
  class UserRepositoryTest {

      @Autowired
      private UserRepository userRepository;

      @Test
      void findByEmail_shouldReturnUser() {
          User user = new User(null, "Max", "max@test.de");
          userRepository.save(user);

          Optional<User> found = userRepository.findByEmail("max@test.de");

          assertTrue(found.isPresent());
          assertEquals("Max", found.get().getName());
      }
  }

TEST BEST PRACTICES
-------------------
  1. AAA-Pattern befolgen
     - Arrange: Test-Setup
     - Act: Zu testende Aktion
     - Assert: Ergebnis pruefen

  2. Ein Konzept pro Test
     - Nicht mehrere unabhaengige Dinge testen
     - Klare, fokussierte Tests

  3. Aussagekraeftige Namen
     - methodName_shouldDoX_whenConditionY
     - Oder: @DisplayName verwenden

  4. Tests sind Dokumentation
     - Tests zeigen erwartetes Verhalten
     - Leser versteht API durch Tests

  5. Keine Test-Interdependenzen
     - Jeder Test muss isoliert laufen
     - Reihenfolge darf nicht relevant sein

  6. Schnelle Tests
     - Unit Tests < 100ms
     - Slow Tests separat markieren (@Tag("slow"))

  7. Mocking sparsam einsetzen
     - Nur externe Abhaengigkeiten mocken
     - Nicht das Testobjekt selbst mocken

TESTCONTAINERS
--------------
Echte Container fuer Integrationstests:

  @SpringBootTest
  @Testcontainers
  class UserRepositoryIntegrationTest {

      @Container
      static PostgreSQLContainer<?> postgres =
          new PostgreSQLContainer<>("postgres:15")
              .withDatabaseName("testdb");

      @DynamicPropertySource
      static void configureProperties(DynamicPropertyRegistry registry) {
          registry.add("spring.datasource.url", postgres::getJdbcUrl);
          registry.add("spring.datasource.username", postgres::getUsername);
          registry.add("spring.datasource.password", postgres::getPassword);
      }

      @Autowired
      private UserRepository userRepository;

      @Test
      void shouldPersistUser() {
          User user = new User(null, "Max", "max@test.de");
          User saved = userRepository.save(user);

          assertNotNull(saved.getId());
      }
  }

ABHAENGIGKEITEN (MAVEN)
-----------------------
  <dependency>
      <groupId>org.junit.jupiter</groupId>
      <artifactId>junit-jupiter</artifactId>
      <version>5.10.0</version>
      <scope>test</scope>
  </dependency>

  <dependency>
      <groupId>org.mockito</groupId>
      <artifactId>mockito-junit-jupiter</artifactId>
      <version>5.7.0</version>
      <scope>test</scope>
  </dependency>

  <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-test</artifactId>
      <scope>test</scope>
  </dependency>

SIEHE AUCH
==========
  wiki/java/README.txt           Java Uebersicht
  wiki/java/spring/README.txt    Spring Framework
  wiki/automatisierung/code_testing.txt  Test-Automatisierung
