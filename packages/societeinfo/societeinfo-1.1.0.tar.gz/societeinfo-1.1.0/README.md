# SOCIETE INFO

Python wrapper to SOCIETE INFO api.

SOCIETE INFO is a french company providing access to french companies data.

To learn more, you can take a look at:

- [Corporate website](https://societeinfo.com)
- [API documentation](https://societeinfo.com/api-doc/#introduction)

## Installation

```shell
pip install societeinfo
```

## Run tests

```shell
pip install -e '.[dev]'
pytest
```

## Usage

```python
import societeinfo

# Init api client
societeinfo_client = societeinfo.SocieteInfoClient(api_key='YOUR API KEY')

# Get credit details
societeinfo_client.get_credit_details()

# Autocomplete companies
companies = societeinfo_client.autocomplete_companies('Emmaüs')

# Get a company
company = societeinfo_client.get_company_by_id(companies['result'][0]['id'])
```
