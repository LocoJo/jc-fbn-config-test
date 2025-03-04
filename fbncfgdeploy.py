# Set up LUSID
import os
from os import environ
import pandas as pd
import json
import uuid
import pytz
from datetime import datetime, timedelta

import logging
logging.basicConfig(level=logging.INFO)

import lusid as lu
import lusid.api as la
import lusid.models as lm

from lusid.utilities import ApiClientFactory
from lusidjam import RefreshingToken

# fbn config
from fbnconfig import drive
from fbnconfig import Deployment, deploy

# Set pandas display options
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.options.display.float_format = "{:,.2f}".format

# Authenticate to SDK
# Run the Notebook in Jupyterhub for your LUSID domain and authenticate automatically
secrets_path = os.getenv("FBN_SECRETS_PATH")

# Run the Notebook locally using a secrets file (see https://support.lusid.com/knowledgebase/article/KA-01663)
if secrets_path is None:
    secrets_path = os.path.join(os.path.dirname(os.getcwd()), "secrets.json")

api_factory = ApiClientFactory(
    token=RefreshingToken(),
    api_secrets_filename=secrets_path,
    app_name="VSCode"
)

def configure(env):
    f1 = drive.FolderResource(id="base_folder", name="my_folder", parent=drive.root)
    return Deployment("my_deployment", [f1])

host_vars = {} # I think this is just dictionary representation of vars file.
lusid_url = os.getenv("LUSID_ENV")
token = api_factory.api_client.configuration.access_token
deployment = configure(host_vars)

# Deploy via existing deployment procedure.
import properties
properties.main(api_factory)

# Deploy fbn config
deploy(deployment, lusid_url, token)