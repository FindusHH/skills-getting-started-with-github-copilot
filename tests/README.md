# Tests für Mergington High School Activities API

Dieses Verzeichnis enthält eine umfassende Test-Suite für die FastAPI-Anwendung.

## Test-Struktur

### `test_api.py`
- **TestMainEndpoints**: Tests für Haupt-API-Endpunkte
  - Root-Redirect-Funktionalität
  - Abrufen aller Aktivitäten
  
- **TestSignupEndpoint**: Tests für Student-Anmeldung
  - Erfolgreiche Anmeldung
  - Anmeldung für nicht existierende Aktivitäten
  - Doppelte Anmeldung verhindern
  - Sonderzeichen in E-Mails
  
- **TestUnregisterEndpoint**: Tests für Student-Abmeldung
  - Erfolgreiche Abmeldung
  - Abmeldung von nicht existierenden Aktivitäten
  - Abmeldung nicht registrierter Studenten
  
- **TestIntegrationScenarios**: Integrationstests
  - Vollständiger Anmelde-/Abmelde-Workflow
  - Mehrere Studenten für dieselbe Aktivität

### `test_validation.py`
- **TestDataValidation**: Tests für Datenvalidierung
  - Leere E-Mail-Parameter
  - URL-kodierte Aktivitätsnamen
  - Groß-/Kleinschreibung bei Aktivitätsnamen
  
- **TestErrorHandling**: Tests für Fehlerbehandlung
  - Fehlende Parameter
  - Ungültige HTTP-Methoden
  
- **TestBoundaryConditions**: Tests für Grenzfälle
  - Sehr lange E-Mail-Adressen
  - Sonderzeichen in E-Mails
  - URL-Encoding-Verhalten

### `conftest.py`
Enthält gemeinsame Test-Fixtures:
- `client`: TestClient für die FastAPI-Anwendung
- `reset_activities`: Zurücksetzen der Aktivitätsdaten vor jedem Test

## Tests ausführen

### Alle Tests ausführen
```bash
pytest tests/ -v
```

### Tests mit Coverage-Bericht
```bash
pytest tests/ --cov=src --cov-report=html --cov-report=term
```

### Spezifische Test-Datei ausführen
```bash
pytest tests/test_api.py -v
```

### Spezifischen Test ausführen
```bash
pytest tests/test_api.py::TestSignupEndpoint::test_successful_signup -v
```

## Coverage-Berichte

Die Tests erreichen 100% Codeabdeckung der `src/app.py` Datei.

HTML-Coverage-Berichte werden im `htmlcov/` Verzeichnis generiert und können im Browser geöffnet werden:
```bash
open htmlcov/index.html
```

## Test-Abhängigkeiten

- `pytest`: Test-Framework
- `httpx`: HTTP-Client für API-Tests
- `pytest-cov`: Coverage-Berichte
- `fastapi.testclient`: TestClient für FastAPI

Alle Abhängigkeiten sind in der `requirements.txt` aufgelistet.