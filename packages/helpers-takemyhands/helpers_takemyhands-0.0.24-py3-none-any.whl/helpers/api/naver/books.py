import requests

def get_books_by_query(query, **kwargs):
    headers = kwargs.get("headers", None)
    display = kwargs.get("display", 10)
    start = kwargs.get("start", 1)
    sort = kwargs.get("sort", "count")

    base_url = "https://openapi.naver.com/"
    prefix = "v1/search/book.json?"
    full_url = f"{base_url}{prefix}&query={query}&display={display}&start={start}&sort={sort}"
    return requests.get(full_url, headers=headers)