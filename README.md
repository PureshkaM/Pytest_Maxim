# Pytest_Maxim

Набор автотестов REST API на **pytest** с валидацией ответов через **pydantic**.
В качестве тестируемого сервиса используется публичный
[Met Museum Collection API](https://collectionapi.metmuseum.org/public/collection/v1).

## Что внутри

- `models.py` — pydantic-модели ответов API (`ObjectsList`, `ArtObject`, `SearchResponse`,
  `DepartmentsResponse`, `Constituent`): контракт, по которому проверяется структура и типы полей.
- `tests.py` — тесты эндпоинтов с session-scoped фикстурой логирования и замером времени ответа.

Проверяется не только код ответа, но и соответствие тела ответа схеме — то есть
несовпадение типа или пропавшее поле роняет тест, а не проходит незамеченным.

## Запуск

```bash
pip install pytest requests pydantic
pytest tests.py -v
```
