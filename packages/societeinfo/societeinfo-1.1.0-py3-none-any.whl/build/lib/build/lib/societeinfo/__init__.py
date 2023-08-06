# -*- coding: utf-8 -*-
import requests

from societeinfo.exceptions import NoApiKeyProvidedError


class SocieteInfoClient(object):
    """
    Client object made to process requests to SOCIETE INFO api.
    """
    _SOCIETE_INFO_BASE_URL = 'https://societeinfo.com/app/rest/api/v2'

    def __init__(self, api_key):
        self._api_key = api_key
        if not self._api_key:
            raise NoApiKeyProvidedError('You must provide a valid api key.')

    def _get(self, url_path, query_params=None):
        """
        Generic method to make HTTP calls.

        :param str url_path: URL path concatenated to service "base URL".
        :param dict query_params: Query parameters.
        :rtype: dict
        """
        response = requests.get(
            url=self._SOCIETE_INFO_BASE_URL + url_path,
            params=query_params,
            headers={'X-API-KEY': self._api_key},
        )
        response.raise_for_status()
        return response.json()

    def autocomplete_companies(
            self,
            search,
            limit=10,
            page=1,
            include_inactive_companies=True,
            include_establishments=False,
    ):
        """
        Autocomplete companies from a given search.

        Documentation reference: https://societeinfo.com/api-doc/#autocomplete-company
        Pricing for this call: 0 credits.

        :param str search: Company name or SIREN/SIRET search, two characters minimum.
        :param int limit: Maximum number of results to be retrieved (per page), limited to 25.
        :param int page: Page number of results, starting by default to 1.
        :param bool include_inactive_companies: Whether inactive companies should be included or not.
        :param bool include_establishments: Whether establishments should be included or not.
        :rtype: dict
        """
        return self._get(
            url_path='/companies.json/autocomplete',
            query_params={
                'query': search,
                'limit': limit,
                'page': page,
                'active': include_inactive_companies,
                'withEstablishments': include_establishments,
            },
        )

    def get_company_by_id(self, company_id, include_establishments=False):
        """
        Get a company from its SOCIETE INFO identifier.

        Documentation reference: https://societeinfo.com/api-doc/#get-company
        Pricing for this call: 1 credit / success.

        :param str company_id: SOCIETE INFO identifier.
        :param bool include_establishments: Whether establishments should be included or not.
        :rtype: dict
        """
        return self._get(
            url_path='/company.json/{}'.format(company_id or ''),
            query_params={
                'withEstablishments': include_establishments
            },

        )

    def get_credit_details(self):
        """
        Get credits details.

        See https://societeinfo.com/tarifs/ to learn more about pricing.

        Documentation reference: https://societeinfo.com/api-doc/#credits
        Pricing for this call: 0 credits.

        :rtype: dict
        """
        return self._get(
            url_path='/apikeyinfo.json',
        )
