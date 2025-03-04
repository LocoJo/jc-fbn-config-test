import fbnconfig
import os
import logging
from lusid.utilities import ApiClientFactory

logging.basicConfig(level=logging.INFO)

secrets_path = os.getenv("FBN_SECRETS_PATH")
lusid_env = os.getenv("LUSID_ENV")

if secrets_path is None:
    secrets_path = os.path.join(os.path.dirname(os.getcwd()), "secrets.json")

api_factory = ApiClientFactory(
    api_secrets_filename=secrets_path,
    app_name="FbnConfigOts"
)

token = api_factory.api_client.configuration.access_token
client = fbnconfig.create_client(lusid_env, token)
fbnconfig.setup(client)