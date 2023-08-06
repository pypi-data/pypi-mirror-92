import pytest
import requests
import requests_mock

import societeinfo


def test_get_company_by_id_ok():
    societeinfo_client = societeinfo.SocieteInfoClient(api_key='some fake api key')

    with requests_mock.mock() as m:
        m.get(
            'https://societeinfo.com/app/rest/api/v2/company.json/112358',
            json={'fake': 'result'},
            status_code=200,
        )

        company = societeinfo_client.get_company_by_id('112358')

    assert company == {'fake': 'result'}
    assert m.call_count == 1
    assert len(m.request_history) == 1
    assert m.request_history[0].headers['X-API-KEY'] == 'some fake api key'


def test_get_company_by_id_not_found():
    societeinfo_client = societeinfo.SocieteInfoClient(api_key='some fake api key')

    with requests_mock.mock() as m:
        m.get(
            'https://societeinfo.com/app/rest/api/v2/company.json/112358',
            json={'fake': 'result'},
            status_code=404,
        )

        with pytest.raises(requests.exceptions.HTTPError):
            societeinfo_client.get_company_by_id('112358')

    assert m.call_count == 1
    assert len(m.request_history) == 1
    assert m.request_history[0].headers['X-API-KEY'] == 'some fake api key'
