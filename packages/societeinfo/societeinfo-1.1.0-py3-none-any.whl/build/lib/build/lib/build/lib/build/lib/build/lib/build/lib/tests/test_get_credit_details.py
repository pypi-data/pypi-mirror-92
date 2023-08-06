import requests_mock

import societeinfo


def test_get_credit_details():
    societeinfo_client = societeinfo.SocieteInfoClient(api_key='some fake api key')

    with requests_mock.mock() as m:
        m.get(
            'https://societeinfo.com/app/rest/api/v2/apikeyinfo.json',
            json={'fake': 'result'},
            status_code=200,
        )

        credit_details = societeinfo_client.get_credit_details()

    assert credit_details == {'fake': 'result'}
    assert m.call_count == 1
    assert len(m.request_history) == 1
    assert m.request_history[0].headers['X-API-KEY'] == 'some fake api key'
