# BACH Ollama Tools

Tools für die Integration mit Ollama (lokale LLMs).

## Enthaltene Tools

| Tool | Zweck |
|------|-------|
| `ollama_client.py` | Ollama API Client |
| `ollama_benchmark.py` | Performance-Benchmarks |
| `ollama_summarize.py` | Text-Zusammenfassung |
| `ollama_worker.py` | Background Worker |

## Konfiguration

Ollama muss lokal installiert und gestartet sein:
- Default URL: `http://localhost:11434`

## Nutzung

```bash
# Client testen
python skills/tools/ollama/ollama_client.py --test

# Benchmark
python skills/tools/ollama/ollama_benchmark.py
```

---

*BACH v1.1 - Ollama Tools*