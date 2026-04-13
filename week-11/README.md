# Week 11 - Testing (E-commerce Backend)

This week focuses on automated testing for the Flask e-commerce backend.

## Goals

- Add unit tests for core logic and utilities.
- Add API integration tests for routes and business rules.
- Achieve 80%+ test coverage for backend source files.
- Provide Postman integration tests with assertions.
- Demonstrate mocking of external dependencies.

## What Was Added

- Pytest test suite under `tests/`:
   - `test_unit_core.py` for auth/crud/image utility logic.
   - `test_api_integration.py` for end-to-end API flows.
   - `test_api_branches.py` for route validation and edge branches.
   - `test_main_and_serializers.py` for app handlers and serializer helpers.
   - `conftest.py` for isolated DB/app fixtures.
- Coverage configuration in `pytest.ini`.
- Postman collection with test scripts: `postman_week11_tests_collection.json`.
- Coverage report template: `TEST_COVERAGE_REPORT.md`.

## Test Stack

- `pytest`
- `pytest-cov`
- Flask test client + SQLite test DB
- `monkeypatch` for mocking external-like dependencies

## Mocking Example

External dependency mocking is implemented in tests like:

- `tests/test_api_integration.py` where `routes.image_routes.save_product_image` is monkeypatched.
- This simulates an external image-processing service and validates route behavior without file/image backend coupling.

## Run Locally

1. Install deps:

```bash
cd week-11
pip install -r requirements.txt
```

2. Run tests with coverage:

```bash
python -m pytest
```

3. Optional detailed coverage output:

```bash
python -m pytest --cov=. --cov-report=term-missing --cov-report=xml
```

## Postman Integration Tests

Import:

- `postman_week11_tests_collection.json`

It includes response assertions for:

- Auth flow
- Category/Product creation flow
- Image upload flow
- Aggregation and health endpoints

### Run via Newman (optional)

```bash
npm install -g newman
newman run postman_week11_tests_collection.json
```

## Deliverables

- Unit and integration tests in `tests/`
- Coverage configuration and generated XML (`coverage.xml`)
- Coverage report summary in `TEST_COVERAGE_REPORT.md`
- Postman integration tests in `postman_week11_tests_collection.json`
