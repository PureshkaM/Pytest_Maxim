import logging
import requests
import pytest
import time

from models import (
    ArtObject,
    SearchResponse,
    ObjectsList,
    DepartmentsResponse
)

API = "https://collectionapi.metmuseum.org/public/collection/v1"



# Логирование
@pytest.fixture(scope="session")
def logger():
    logger = logging.getLogger("tests")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )
    file_handler = logging.FileHandler("tests.log", mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.propagate = False
    return logger

def log_request(logger, method, url, response, start_time):
    elapsed = time.time() - start_time
    try:
        body = response.json()
    except Exception:
        body = response.text
    logger.info(
        "\n"
        f"--- HTTP REQUEST -----------------------------\n"
        f"METHOD: {method}\n"
        f"URL: {url}\n"
        f"STATUS: {response.status_code}\n"
        f"TIME: {elapsed:.3f} s\n"
        f"RESPONSE HEADERS: {response.headers}\n"
        f"RESPONSE BODY:\n{body}\n"
        f"----------------------------------------------"
    )



#TEST /objects/{id}
def test_get_object_success(logger):
    object_id = 1
    url = f"{API}/objects/{object_id}"
    logger.info(f"GET {url}")
    response = requests.get(url)
    assert response.status_code == 200
    try:
        data = ArtObject(**response.json())
        logger.info(f"Validated ArtObject: {data}")
    except Exception as e:
        logger.error(f"Validation error: {e}")
        raise


def test_get_object_not_found(logger):
    object_id = 999999999
    url = f"{API}/objects/{object_id}"
    logger.info(f"GET {url}")
    start = time.time()
    response = requests.get(url)
    log_request(logger, "GET", url, response, start)
    assert response.status_code in (200, 404)
    if response.status_code == 200:
        body = response.json()
        assert "objectID" not in body



#TEST /search
def test_search_results(logger):
    keyword = "sunflower"
    url = f"{API}/search?q={keyword}"
    logger.info(f"GET {url}")
    start = time.time()
    response = requests.get(url)
    log_request(logger, "GET", url, response, start)
    assert response.status_code == 200
    data = SearchResponse(**response.json())
    logger.info(f"Search returned {data.total} results")
    if data.objectIDs:
        assert isinstance(data.objectIDs, list)

def test_search_limit(logger):
    url = f"{API}/search?q=art"
    logger.info(f"GET {url}")
    start = time.time()
    response = requests.get(url)
    log_request(logger, "GET", url, response, start)
    assert response.status_code == 200
    data = SearchResponse(**response.json())
    logger.info(f"Search returned total={data.total}")
    assert data.total <= 1_000_000



#TEST /objects
def test_objects_list(logger):
    url = f"{API}/objects"
    logger.info(f"GET {url}")
    start = time.time()
    response = requests.get(url)
    log_request(logger, "GET", url, response, start)
    assert response.status_code == 200
    data = ObjectsList(**response.json())
    assert data.total > 0
    assert isinstance(data.objectIDs, list)
    assert len(data.objectIDs) > 0



#TEST /departments
def test_departments(logger):
    url = f"{API}/departments"
    logger.info(f"GET {url}")
    start = time.time()
    response = requests.get(url)
    log_request(logger, "GET", url, response, start)
    assert response.status_code == 200
    data = DepartmentsResponse(**response.json())
    assert len(data.departments) > 0

    for dep in data.departments:
        assert dep.departmentId > 0
        assert isinstance(dep.displayName, str)



#TEST Проверка стабильности порядка результатов
def test_search_result_order_is_stable(logger):
    url = f"{API}/search?q=sunflower"
    logger.info(f"GET {url}")
    start = time.time()
    r1 = requests.get(url)
    log_request(logger, "GET", url, r1, start)
    start = time.time()
    r2 = requests.get(url)
    log_request(logger, "GET", url, r2, start)
    assert r1.status_code == 200 and r2.status_code == 200
    d1 = SearchResponse(**r1.json())
    d2 = SearchResponse(**r2.json())
    if d1.objectIDs and d2.objectIDs:
        assert d1.objectIDs[:20] == d2.objectIDs[:20]