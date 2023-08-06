import pytest

import societeinfo
from societeinfo.exceptions import NoApiKeyProvidedError


def test_societeinfoclient_class_init_ok():
    societeinfo_client = societeinfo.SocieteInfoClient(api_key='some fake api key')

    assert isinstance(societeinfo_client, societeinfo.SocieteInfoClient)
    assert societeinfo_client._api_key == 'some fake api key'


@pytest.mark.parametrize('api_key', [
    None,
    '',
])
def test_societeinfoclient_class_init_no_api_key_provided(api_key):
    with pytest.raises(NoApiKeyProvidedError):
        societeinfo.SocieteInfoClient(api_key=api_key)
