Между тремя вариантами - Flask, FastAPI, Django - выбор очевиден, это FastAPI, потому что он обеспечивает нативную асинхронность, что полезно для высоконагруженных сервисов, и автоматически генерирует OpenAPI-документацию. Flask проще для старта, но требует ручной настройки, а Django избыточен для этой задачи


| | Flask | FastAPI | Django |
| :---: | :---: | :---: | :--- |
| Footprint | minimal | moderate | large |
| async support | sync only | async/await | mostly sync |
| Docs | manual | auto (OpenAPI) | manual |
| Learning curve | low | medium | high |