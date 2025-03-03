import fbnconfig
import os
from lusidjam import RefreshingToken
# Set up LUSID
import pandas as pd
import json
import uuid
import pytz
from datetime import datetime, timedelta
import json

import logging
logging.basicConfig(level=logging.INFO)

import lusid as lu
import lusid.api as la
import lusid.models as lm
import lusid.exceptions as le

from lusid.utilities import ApiClientFactory

# Authenticate to SDK
# Run the Notebook in Jupyterhub for your LUSID domain and authenticate automatically
secrets_path = os.getenv("FBN_SECRETS_PATH")
lusid_env = os.getenv("LUSID_ENV")

# Run the Notebook locally using a secrets file (see https://support.lusid.com/knowledgebase/article/KA-01663)
if secrets_path is None:
    secrets_path = os.path.join(os.path.dirname(os.getcwd()), "secrets.json")

api_factory = ApiClientFactory(
    token=RefreshingToken(),
    api_secrets_filename=secrets_path,
    app_name="FbnConfigOts"
)

token = api_factory.api_client.configuration.access_token
client = fbnconfig.create_client(lusid_env, token)
fbnconfig.setup(client)