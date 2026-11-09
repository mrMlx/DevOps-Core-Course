> *This document provides explanations in two languages: Russian (native) and English.*

## Framework Selection

> RU:
Между тремя вариантами - Flask, FastAPI, Django - выбор очевиден, это FastAPI, потому что он обеспечивает нативную асинхронность, что полезно для высоконагруженных сервисов, и автоматически генерирует OpenAPI-документацию. Flask проще для старта, но требует ручной настройки, а Django избыточен для этой задачи.

> ENG:
Among the three options — Flask, FastAPI, and Django — the choice is obvious: FastAPI. It provides native asynchronous support, which is highly beneficial for high-load services, and automatically generates OpenAPI documentation. Flask is easier for a start but requires manual configuration, while Django is overkill for this specific task.


| | Flask | FastAPI | Django |
| :---: | :---: | :---: | :--- |
| Footprint | minimal | moderate | large |
| async support | sync only | async/await | mostly sync |
| Docs | manual | auto (OpenAPI) | manual |
| Learning curve | low | medium | high |

## Best Practiсes Applied
> RU:
*   **Переменные среды:** Использованы для конфигурации (HOST, PORT, DEBUG), чтобы следовать принципам 12-факторного приложения и обеспечить работу в любом окружении без изменения кода.
*   **Кастомные обработчики ошибок:** Реализованы JSON-ответы для ошибок 404 и 500, чтобы API всегда оставалось консистентным для клиентов.
*   **Гигиена кода:** Добавлены `.gitignore` и `requirements.txt` для поддержания чистоты репозитория и воспроизводимости окружения.
*   **Соответствие PEP 8:** Импорты сгруппированы по стандарту (стандартная библиотека, сторонние, локальные) для лучшей читаемости.

> ENG:
*   **Environment Variables:** Used for configuration (`HOST`, `PORT`, `DEBUG`) to follow 12-factor app principles and ensure the app runs in any environment without code changes.
*   **Custom Error Handlers:** Implemented JSON responses for 404 and 500 errors to keep the API consistent and predictable for clients.
*   **Code Hygiene:** Added `.gitignore` and `requirements.txt` to maintain a clean repository and ensure environment reproducibility.
*   **PEP 8 Compliance:** Grouped imports by standard (stdlib, third-party, local) for better code readability.
## API Documentation
| Method | Path | Description |
| :--- | :--- | :--- |
| GET | '/' | Returns full service and system info|
| GET | '/health' | Health check endpoint |

## Testing Evidence

### 1)
> curl.exe -s http://localhost:5000/
```
{"service":{"name":"my-devops-service","version":"1.0.0","description":"FastAPI application for DevOps lab","framework":"FastAPI"},"system":{"hostname":"WIN-3SURHTUNL9B","platform":"Windows","platform_version":"10.0.26200","architecture":["64bit","WindowsPE"],"cpu_count":16,"python_version":"3.14.6"},"runtime":{"uptime_seconds":178,"uptime_human":"0 hour, 2 minutes","current_time":"2026-11-08T12:04:36.402246+00:00","timezone":"UTC"},"request":{"client_ip":"127.0.0.1","user_agent":"curl/8.21.0","method":"GET","path":"/"},"endpoints":[{"path":"/","method":"GET","description":"Returns full service and system info"},{"path":"/health","method":"GET","description":"Health check endpoint"}]}
```
---
### 2)
> curl.exe -s http://localhost:5000/health
```
{"status":"ok","timestamp":"2026-11-08T12:06:58.569643+00:00","uptime_seconds":321}
```
---
### 3)
> curl.exe -s http://localhost:5000/abracadabra
```
{"error":"Not Found","status":"error","path":"/abracadabra"}
```
-----
> curl.exe -s -o NUL -w "HTTP %{http_code}\n" http://localhost:5000/abracadabra
```
HTTP 404
```
---
### 4)
> $env:PORT=8080; python main.py
```
2026-11-08 15:22:38,340 - INFO - Application started
INFO:     Started server process [12136]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```
---
## Challanges & Solutions
> RU:
Одной из проблем было адаптировать команды под Windows powershell, справился с этим с помощью поиска в браузере. Также была проблема с подсчетом uptime, решил с помощью дельты текущего времени и времени запуска, а также с помощью методов дельты и математических операций для поиска часов и минут из секунд.

> ENG:
One of the biggest challenges was adapting the Linux-based commands for Windows PowerShell, which I resolved through web research. Additionally, I faced a logic issue with calculating the human-readable uptime. I solved this by calculating the timedelta between the current time and the start time, and then applying arithmetic operations (modulo and integer division) to correctly extract hours and minutes from total seconds.

## GitHub Community