# Portabilitaet: UNIVERSAL
# Zuletzt validiert: 2026-02-05 (Claude/BACH wiki-author)
# Naechste Pruefung: 2027-02-05
# Quellen: docs.python.org/3/library/tkinter.html, doc.qt.io, kivy.org, wxpython.org

GUI-PROGRAMMIERUNG MIT PYTHON
=============================

Stand: 2026-02-05

UEBERBLICK
==========
  Python bietet mehrere Bibliotheken zur Erstellung grafischer
  Benutzeroberflaechen (GUIs). Die Wahl haengt von Anforderungen
  wie Komplexitaet, Aussehen und Plattformunterstuetzung ab.

  Hauptoptionen:
    - Tkinter       Standard-Bibliothek, einfach, portabel
    - PyQt/PySide   Professionell, umfangreich, Qt-basiert
    - Kivy          Touch/Mobile, modern, GPU-beschleunigt
    - wxPython      Native Widgets, Desktop-Anwendungen
    - Dear PyGui    Schnell, GPU-gerendert, fuer Tools

BIBLIOTHEKEN-VERGLEICH
======================

  | Bibliothek | Einsteiger | Aussehen   | Plattformen     | Lizenz      |
  |------------|------------|------------|-----------------|-------------|
  | Tkinter    | Einfach    | Basic      | Win/Mac/Linux   | PSF (frei)  |
  | PyQt6      | Mittel     | Modern     | Win/Mac/Linux   | GPL/Kommerz |
  | PySide6    | Mittel     | Modern     | Win/Mac/Linux   | LGPL        |
  | Kivy       | Mittel     | Eigen      | +Mobile/Touch   | MIT         |
  | wxPython   | Mittel     | Nativ      | Win/Mac/Linux   | wxWindows   |
  | Dear PyGui | Einfach    | Modern     | Win/Mac/Linux   | MIT         |

TKINTER - STANDARD GUI
======================

GRUNDSTRUKTUR
-------------
  import tkinter as tk
  from tkinter import ttk  # Modernere Widgets

  # Hauptfenster erstellen
  root = tk.Tk()
  root.title("Meine Anwendung")
  root.geometry("400x300")  # Breite x Hoehe

  # Widget hinzufuegen
  label = ttk.Label(root, text="Hallo Welt!")
  label.pack(pady=20)

  # Event-Loop starten
  root.mainloop()

WIDGETS (STEUERELEMENTE)
------------------------
  import tkinter as tk
  from tkinter import ttk

  root = tk.Tk()
  root.title("Widget Demo")

  # Label (Text)
  label = ttk.Label(root, text="Ein Label")
  label.pack()

  # Button
  def button_click():
      label.config(text="Button geklickt!")

  button = ttk.Button(root, text="Klick mich", command=button_click)
  button.pack()

  # Eingabefeld
  entry = ttk.Entry(root, width=30)
  entry.pack()
  entry.insert(0, "Standardtext")

  # Mehrzeiliger Text
  text = tk.Text(root, height=5, width=40)
  text.pack()
  text.insert("1.0", "Mehrzeiliger Text hier...")

  # Checkbox
  check_var = tk.BooleanVar()
  checkbox = ttk.Checkbutton(root, text="Option", variable=check_var)
  checkbox.pack()

  # Radiobuttons
  radio_var = tk.StringVar(value="option1")
  radio1 = ttk.Radiobutton(root, text="Option 1", variable=radio_var, value="option1")
  radio2 = ttk.Radiobutton(root, text="Option 2", variable=radio_var, value="option2")
  radio1.pack()
  radio2.pack()

  # Dropdown (Combobox)
  combo = ttk.Combobox(root, values=["Auswahl 1", "Auswahl 2", "Auswahl 3"])
  combo.current(0)
  combo.pack()

  # Listbox
  listbox = tk.Listbox(root, height=4)
  for item in ["Eintrag 1", "Eintrag 2", "Eintrag 3"]:
      listbox.insert(tk.END, item)
  listbox.pack()

  # Slider
  scale = ttk.Scale(root, from_=0, to=100, orient="horizontal")
  scale.pack()

  # Progressbar
  progress = ttk.Progressbar(root, length=200, mode='determinate')
  progress.pack()
  progress['value'] = 50

  root.mainloop()

LAYOUT-MANAGER
--------------
  # 1. PACK - Einfach, stapelt Widgets
  widget.pack()                          # Standard
  widget.pack(side="left")               # Links anordnen
  widget.pack(fill="x")                  # Horizontal fuellen
  widget.pack(fill="both", expand=True)  # Voll ausdehnen
  widget.pack(padx=10, pady=5)           # Abstand

  # 2. GRID - Tabellen-Layout
  label.grid(row=0, column=0)
  entry.grid(row=0, column=1)
  button.grid(row=1, column=0, columnspan=2)  # 2 Spalten
  widget.grid(sticky="nsew")  # An allen Seiten anheften

  # 3. PLACE - Absolute Positionierung (selten verwendet)
  widget.place(x=100, y=50)
  widget.place(relx=0.5, rely=0.5, anchor="center")  # Zentriert

BEISPIEL: GRID-LAYOUT
---------------------
  import tkinter as tk
  from tkinter import ttk

  root = tk.Tk()
  root.title("Anmeldeformular")

  # Grid konfigurieren
  root.columnconfigure(1, weight=1)

  # Zeile 0: Benutzername
  ttk.Label(root, text="Benutzername:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
  user_entry = ttk.Entry(root)
  user_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

  # Zeile 1: Passwort
  ttk.Label(root, text="Passwort:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
  pass_entry = ttk.Entry(root, show="*")
  pass_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

  # Zeile 2: Button
  ttk.Button(root, text="Anmelden").grid(row=2, column=0, columnspan=2, pady=10)

  root.mainloop()

EVENTS UND CALLBACKS
--------------------
  import tkinter as tk

  root = tk.Tk()

  # Button-Callback
  def on_button_click():
      print("Button geklickt")

  button = tk.Button(root, text="Klick", command=on_button_click)
  button.pack()

  # Event-Binding
  def on_key(event):
      print(f"Taste gedrueckt: {event.char}")

  def on_enter(event):
      print("Maus ueber Widget")

  root.bind("<Key>", on_key)
  button.bind("<Enter>", on_enter)      # Maus betritt
  button.bind("<Leave>", lambda e: print("Maus verlaesst"))

  # Wichtige Events:
  # <Button-1>     Linksklick
  # <Button-3>     Rechtsklick
  # <Double-1>     Doppelklick
  # <Return>       Enter-Taste
  # <Escape>       Escape-Taste
  # <Control-s>    Strg+S
  # <Motion>       Mausbewegung

  root.mainloop()

DIALOGE
-------
  from tkinter import messagebox, filedialog, colorchooser, simpledialog

  # Nachrichtenboxen
  messagebox.showinfo("Info", "Hier ist eine Information")
  messagebox.showwarning("Warnung", "Achtung!")
  messagebox.showerror("Fehler", "Ein Fehler ist aufgetreten")

  # Ja/Nein Dialog
  antwort = messagebox.askyesno("Frage", "Moechten Sie fortfahren?")
  if antwort:
      print("Ja gewaehlt")

  # Datei oeffnen
  datei = filedialog.askopenfilename(
      title="Datei auswaehlen",
      filetypes=[("Textdateien", "*.txt"), ("Alle", "*.*")]
  )

  # Datei speichern
  datei = filedialog.asksaveasfilename(
      defaultextension=".txt",
      filetypes=[("Textdateien", "*.txt")]
  )

  # Ordner auswaehlen
  ordner = filedialog.askdirectory()

  # Farbauswahl
  farbe = colorchooser.askcolor(title="Farbe waehlen")

  # Eingabedialog
  name = simpledialog.askstring("Eingabe", "Ihr Name:")
  zahl = simpledialog.askinteger("Eingabe", "Eine Zahl:", minvalue=0, maxvalue=100)

KOMPLETTES BEISPIEL: TEXTEDITOR
-------------------------------
  import tkinter as tk
  from tkinter import ttk, filedialog, messagebox

  class TextEditor:
      def __init__(self, root):
          self.root = root
          self.root.title("Einfacher Texteditor")
          self.root.geometry("600x400")
          self.datei_pfad = None

          self.erstelle_menu()
          self.erstelle_editor()

      def erstelle_menu(self):
          menubar = tk.Menu(self.root)
          self.root.config(menu=menubar)

          # Datei-Menu
          datei_menu = tk.Menu(menubar, tearoff=0)
          menubar.add_cascade(label="Datei", menu=datei_menu)
          datei_menu.add_command(label="Neu", command=self.neu, accelerator="Strg+N")
          datei_menu.add_command(label="Oeffnen", command=self.oeffnen, accelerator="Strg+O")
          datei_menu.add_command(label="Speichern", command=self.speichern, accelerator="Strg+S")
          datei_menu.add_separator()
          datei_menu.add_command(label="Beenden", command=self.root.quit)

          # Shortcuts
          self.root.bind("<Control-n>", lambda e: self.neu())
          self.root.bind("<Control-o>", lambda e: self.oeffnen())
          self.root.bind("<Control-s>", lambda e: self.speichern())

      def erstelle_editor(self):
          # Textfeld mit Scrollbar
          frame = ttk.Frame(self.root)
          frame.pack(fill="both", expand=True)

          scrollbar = ttk.Scrollbar(frame)
          scrollbar.pack(side="right", fill="y")

          self.text = tk.Text(frame, yscrollcommand=scrollbar.set, wrap="word")
          self.text.pack(fill="both", expand=True)
          scrollbar.config(command=self.text.yview)

      def neu(self):
          self.text.delete("1.0", tk.END)
          self.datei_pfad = None
          self.root.title("Einfacher Texteditor")

      def oeffnen(self):
          pfad = filedialog.askopenfilename(
              filetypes=[("Textdateien", "*.txt"), ("Alle", "*.*")]
          )
          if pfad:
              with open(pfad, "r", encoding="utf-8") as f:
                  self.text.delete("1.0", tk.END)
                  self.text.insert("1.0", f.read())
              self.datei_pfad = pfad
              self.root.title(f"Texteditor - {pfad}")

      def speichern(self):
          if not self.datei_pfad:
              self.datei_pfad = filedialog.asksaveasfilename(
                  defaultextension=".txt",
                  filetypes=[("Textdateien", "*.txt")]
              )
          if self.datei_pfad:
              with open(self.datei_pfad, "w", encoding="utf-8") as f:
                  f.write(self.text.get("1.0", tk.END))
              messagebox.showinfo("Gespeichert", "Datei wurde gespeichert")

  if __name__ == "__main__":
      root = tk.Tk()
      app = TextEditor(root)
      root.mainloop()

PYQT6 / PYSIDE6 - PROFESSIONELLE GUIS
=====================================

GRUNDSTRUKTUR
-------------
  # PyQt6
  from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
  import sys

  # Oder PySide6 (fast identisch)
  # from PySide6.QtWidgets import QApplication, QMainWindow, QLabel

  class MainWindow(QMainWindow):
      def __init__(self):
          super().__init__()
          self.setWindowTitle("PyQt6 Anwendung")
          self.setGeometry(100, 100, 400, 300)

          label = QLabel("Hallo PyQt!", self)
          label.move(150, 130)

  if __name__ == "__main__":
      app = QApplication(sys.argv)
      window = MainWindow()
      window.show()
      sys.exit(app.exec())

  # Installation: pip install PyQt6
  # Oder:         pip install PySide6

WIDGETS UND LAYOUTS
-------------------
  from PyQt6.QtWidgets import (
      QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
      QLabel, QPushButton, QLineEdit, QTextEdit, QComboBox,
      QCheckBox, QRadioButton, QSlider, QProgressBar
  )
  from PyQt6.QtCore import Qt

  class MainWindow(QMainWindow):
      def __init__(self):
          super().__init__()
          self.setWindowTitle("Widget Demo")

          # Zentrales Widget mit Layout
          central = QWidget()
          self.setCentralWidget(central)
          layout = QVBoxLayout(central)

          # Label
          layout.addWidget(QLabel("Ein Label"))

          # Button
          button = QPushButton("Klick mich")
          button.clicked.connect(self.on_click)
          layout.addWidget(button)

          # Eingabefeld
          self.eingabe = QLineEdit()
          self.eingabe.setPlaceholderText("Text eingeben...")
          layout.addWidget(self.eingabe)

          # Textfeld
          layout.addWidget(QTextEdit())

          # Checkbox
          layout.addWidget(QCheckBox("Option aktivieren"))

          # Dropdown
          combo = QComboBox()
          combo.addItems(["Option 1", "Option 2", "Option 3"])
          layout.addWidget(combo)

          # Slider
          slider = QSlider(Qt.Orientation.Horizontal)
          slider.setRange(0, 100)
          layout.addWidget(slider)

          # Progressbar
          progress = QProgressBar()
          progress.setValue(50)
          layout.addWidget(progress)

      def on_click(self):
          print(f"Eingabe: {self.eingabe.text()}")

SIGNALS UND SLOTS
-----------------
  from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
  from PyQt6.QtCore import pyqtSignal

  class MeinWidget(QWidget):
      # Eigenes Signal definieren
      mein_signal = pyqtSignal(str)

      def __init__(self):
          super().__init__()
          layout = QVBoxLayout(self)

          button = QPushButton("Sende Signal")
          button.clicked.connect(self.sende_signal)
          layout.addWidget(button)

          # Signal mit Slot verbinden
          self.mein_signal.connect(self.empfange_signal)

      def sende_signal(self):
          self.mein_signal.emit("Hallo von Signal!")

      def empfange_signal(self, nachricht):
          print(f"Empfangen: {nachricht}")

KIVY - MOBILE UND TOUCH
=======================

GRUNDSTRUKTUR
-------------
  from kivy.app import App
  from kivy.uix.label import Label
  from kivy.uix.button import Button
  from kivy.uix.boxlayout import BoxLayout

  class MeineApp(App):
      def build(self):
          layout = BoxLayout(orientation='vertical', padding=10)

          self.label = Label(text='Hallo Kivy!')
          layout.add_widget(self.label)

          button = Button(text='Klick mich')
          button.bind(on_press=self.on_button)
          layout.add_widget(button)

          return layout

      def on_button(self, instance):
          self.label.text = 'Button wurde geklickt!'

  if __name__ == '__main__':
      MeineApp().run()

  # Installation: pip install kivy

MIT KV-SPRACHE (DEKLARATIV)
---------------------------
  # main.py
  from kivy.app import App
  from kivy.uix.boxlayout import BoxLayout

  class MeinLayout(BoxLayout):
      def button_click(self):
          self.ids.label.text = "Geklickt!"

  class MeineApp(App):
      def build(self):
          return MeinLayout()

  if __name__ == '__main__':
      MeineApp().run()

  # meine.kv (gleicher Name wie App ohne "App")
  # <MeinLayout>:
  #     orientation: 'vertical'
  #
  #     Label:
  #         id: label
  #         text: 'Hallo Kivy!'
  #
  #     Button:
  #         text: 'Klick mich'
  #         on_press: root.button_click()

DEAR PYGUI - SCHNELLE TOOL-GUIS
===============================

  import dearpygui.dearpygui as dpg

  dpg.create_context()

  def button_callback():
      print("Button geklickt!")

  with dpg.window(label="Hauptfenster", width=400, height=300):
      dpg.add_text("Hallo Dear PyGui!")
      dpg.add_button(label="Klick mich", callback=button_callback)
      dpg.add_input_text(label="Eingabe")
      dpg.add_slider_float(label="Slider", default_value=0.5)
      dpg.add_checkbox(label="Option")

  dpg.create_viewport(title='Meine App', width=600, height=400)
  dpg.setup_dearpygui()
  dpg.show_viewport()
  dpg.start_dearpygui()
  dpg.destroy_context()

  # Installation: pip install dearpygui

BEST PRACTICES
==============

SEPARATION OF CONCERNS
----------------------
  # Model-View-Controller (MVC) Pattern

  # model.py - Datenlogik
  class TodoModel:
      def __init__(self):
          self.todos = []

      def add(self, text):
          self.todos.append({"text": text, "done": False})

      def remove(self, index):
          del self.todos[index]

  # view.py - GUI
  class TodoView:
      def __init__(self, controller):
          self.controller = controller
          # GUI-Aufbau hier

  # controller.py - Verbindet Model und View
  class TodoController:
      def __init__(self):
          self.model = TodoModel()
          self.view = TodoView(self)

THREADING FUER LANGE OPERATIONEN
--------------------------------
  import tkinter as tk
  from tkinter import ttk
  import threading

  class App:
      def __init__(self, root):
          self.root = root

          self.button = ttk.Button(root, text="Starte", command=self.starte_task)
          self.button.pack(pady=10)

          self.progress = ttk.Progressbar(root, mode='indeterminate')
          self.progress.pack(pady=10)

          self.label = ttk.Label(root, text="Bereit")
          self.label.pack()

      def starte_task(self):
          self.button.config(state="disabled")
          self.progress.start()
          self.label.config(text="Arbeite...")

          # Task in separatem Thread
          thread = threading.Thread(target=self.langer_task)
          thread.start()

      def langer_task(self):
          import time
          time.sleep(3)  # Simuliert lange Operation

          # GUI-Update im Hauptthread
          self.root.after(0, self.task_fertig)

      def task_fertig(self):
          self.progress.stop()
          self.button.config(state="normal")
          self.label.config(text="Fertig!")

RESPONSIVE LAYOUTS
------------------
  import tkinter as tk
  from tkinter import ttk

  root = tk.Tk()
  root.title("Responsive Layout")

  # Grid-Gewichtung fuer Skalierung
  root.columnconfigure(0, weight=1)
  root.rowconfigure(1, weight=1)

  # Header (fixe Hoehe)
  header = ttk.Frame(root, height=50)
  header.grid(row=0, column=0, sticky="ew")
  ttk.Label(header, text="Header").pack()

  # Inhalt (skaliert)
  content = ttk.Frame(root)
  content.grid(row=1, column=0, sticky="nsew")
  content.columnconfigure(0, weight=1)
  content.rowconfigure(0, weight=1)

  text = tk.Text(content)
  text.grid(row=0, column=0, sticky="nsew")

  # Footer (fixe Hoehe)
  footer = ttk.Frame(root, height=30)
  footer.grid(row=2, column=0, sticky="ew")
  ttk.Label(footer, text="Statuszeile").pack()

  root.mainloop()

EMPFEHLUNGEN
============

  Fuer Einsteiger / Einfache Tools:
    -> Tkinter (keine Installation noetig)

  Fuer professionelle Desktop-Apps:
    -> PyQt6 oder PySide6

  Fuer Mobile / Touch / Games:
    -> Kivy

  Fuer schnelle Tool-GUIs:
    -> Dear PyGui

  Fuer Web-basierte GUIs:
    -> Streamlit, Gradio, NiceGUI

SIEHE AUCH
==========
  wiki/python/README.txt               Python Uebersicht
  wiki/python/oop/                     Objektorientierung fuer GUI-Klassen
  wiki/python/multithreading/          Threading fuer responsive GUIs
  wiki/webapps/                        Web-basierte Alternativen
