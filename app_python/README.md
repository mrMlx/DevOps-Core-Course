# Overview
This service is based on FastAPI. It returns information about the system (5 keys). Also, it has an endpoint to check health.
Это сревис на FastAPI, он отдает информацию о системе в виде 5 ключей, а также имеет ендпоинт для проверки здоровья.

### Prerequisites
python: 3.14+

OS: Win10/11, Linux

### Instalation
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual evnironment (Windows Powershell)
.\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Running
```bash
# Default run (port 5000)
python app.py

# Custom port (Windows Powershell)
$env:PORT=8080; python app.py
```

### API Endpoints
| Method | Path | Description |
| :--- | :--- | :--- |
| GET | '/' | Returns full service and system info|
| GET | '/health' | Health check endpoint |

### Configuration
| Variable | Default | Purpose |
| :--- | :--- | :--- |
| HOST | '0.0.0.0' | Server bind address|
| PORT | '5000' | Server port |
| DEBUG | 'False' | Enable auto-reload/debug mode |