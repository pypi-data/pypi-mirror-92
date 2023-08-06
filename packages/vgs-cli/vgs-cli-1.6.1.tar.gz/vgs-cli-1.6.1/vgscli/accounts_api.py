import logging

import click
from click import ClickException
from simple_rest_client.api import API
from simple_rest_client.resource import Resource

from vgscli._version import __version__
from vgscli.errors import VaultNotFoundError

logger = logging.getLogger(__name__)

env_url = {
    'dev': 'https://accounts.verygoodsecurity.io',
    'prod': 'https://accounts.apps.verygoodsecurity.com'
}


class AccountsApiResource(Resource):
    actions = {
        'get_vault_by_id': {
            'method': 'GET',
            'url': '/vaults?filter[vaults][identifier]={}',
        }
    }


def create_api(token, environment):
    api = API(
        api_root_url=env_url[environment],
        headers={
            'Content-Type': 'application/vnd.api+json',
            'Accept': 'application/vnd.api+json',
            'User-Agent': 'VGS CLI {}'.format(__version__),
            'Authorization': 'Bearer {}'.format(token)
        },
        timeout=50,  # default timeout in seconds
        append_slash=False,  # append slash to final url
        json_encode_body=True,  # encode body as json
    )

    api.add_resource(resource_name='accounts_api',
                     resource_class=AccountsApiResource)

    return api


def get_api_url(ctx, vault_id, api):
    response = api.accounts_api.get_vault_by_id(vault_id)
    try:
        return response.body['data'][0]['links']['vault_management_api']
    except (KeyError, IndexError):
        # if we weren't able to extract the vault_management_api it means that the provided vault_id doesn't exist
        raise VaultNotFoundError(vault_id, ctx)
