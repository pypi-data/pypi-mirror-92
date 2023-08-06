import requests_mock

import societeinfo


def test_autocomplete_companies_default_arguments():
    societeinfo_client = societeinfo.SocieteInfoClient(api_key='some fake api key')

    with requests_mock.mock() as m:
        m.get(
            'https://societeinfo.com/app/rest/api/v2/companies.json/autocomplete?'
            'query=Emma%C3%BCs&limit=10&page=1&active=True&withEstablishments=False',
            json={'fake': 'result'},
            status_code=200,
        )

        companies = societeinfo_client.autocomplete_companies('Emmaüs')

    assert companies == {'fake': 'result'}
    assert m.call_count == 1
    assert len(m.request_history) == 1
    assert m.request_history[0].headers['X-API-KEY'] == 'some fake api key'


def test_autocomplete_companies_non_default_arguments():
    societeinfo_client = societeinfo.SocieteInfoClient(api_key='some fake api key')

    with requests_mock.mock() as m:
        m.get(
            'https://societeinfo.com/app/rest/api/v2/companies.json/autocomplete?'
            'query=Emma%C3%BCs&limit=7&page=2&active=False&withEstablishments=True',
            json={'fake': 'result'},
            status_code=200,
        )

        companies = societeinfo_client.autocomplete_companies(
            search='Emmaüs',
            limit=7,
            page=2,
            include_inactive_companies=False,
            include_establishments=True,
        )

    assert companies == {'fake': 'result'}
    assert m.call_count == 1
    assert len(m.request_history) == 1
    assert m.request_history[0].headers['X-API-KEY'] == 'some fake api key'
