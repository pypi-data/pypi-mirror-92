import traceback
from concurrent.futures import ThreadPoolExecutor
import requests
from hestia_earth.schema import Bibliography

from .utils import ORINGAL_FIELD, current_time, MAXIMUM_DISTANCE, find_closest_result, remove_empty_values, \
    extend_bibliography


def create_biblio(bibliography: dict, key: str, value: str):
    biblio = Bibliography()
    # save title here since closest bibliography might differ
    biblio.fields[ORINGAL_FIELD + key] = value if bibliography else None
    biblio.fields[key] = value
    authors = bibliography.get('authors', []) if bibliography else []
    (extended_biblio, actors) = extend_bibliography(authors, bibliography.get('year')) if bibliography else ({}, [])
    return (
        {**biblio.to_dict(), **bibliography, **extended_biblio},
        actors
    ) if bibliography else (biblio.to_dict(), [])


def exec_search_by(api_url: str, key: str, value: str):
    return requests.get(f"{api_url}?{key}={value.rstrip()}").json().get('results', [])


def exec_search_by_title(api_url: str, title: str):
    def search(value: str):
        items = exec_search_by(api_url, 'title', value)
        # try a search with shorter value if no results found
        items = items if len(items) > 0 else exec_search_by(api_url, 'title', value[:100])
        return list(map(lambda x: {'title': x.get('title'), 'item': x}, items))

    [bibliography, distance] = find_closest_result(title, search)
    return create_biblio(bibliography if distance <= MAXIMUM_DISTANCE else None, 'title', title)


def exec_search_by_id(api_url: str, value: str):
    return create_biblio(requests.get(f"{api_url}/{value.rstrip()}").json(), 'mendeleyID', value)


def exec_search_by_documentDOI(api_url: str, value: str):
    return create_biblio(exec_search_by(api_url, 'doi', value)[0], 'documentDOI', value)


def exec_search_by_scopus(api_url: str, value: str):
    return create_biblio(exec_search_by(api_url, 'scopus', value)[0], 'scopus', value)


SEARCH_BY_KEY = {
    'title': exec_search_by_title,
    'mendeleyID': exec_search_by_id,
    'documentDOI': exec_search_by_documentDOI,
    'scopus': exec_search_by_scopus
}


def exec_extend(api_url: str, key: str, bibliographies, actors):
    def extend(value: str):
        now = current_time()
        (biblio, authors) = SEARCH_BY_KEY[key](api_url, value)
        print('mendeley', 'find by', key, current_time() - now, value)
        bibliographies.extend([] if biblio is None else [biblio])
        actors.extend([] if authors is None else authors)
    return extend


def extend_mendeley(values, key='title', **kwargs):
    try:
        api_url = kwargs.get('mendeley_api_url')

        bibliographies = []
        actors = []

        extender = exec_extend(api_url, key, bibliographies, actors)
        with ThreadPoolExecutor() as executor:
            executor.map(extender, values)

        return (remove_empty_values(actors), remove_empty_values(bibliographies))
    except Exception:
        print(traceback.format_exc())
        return ([], [])
