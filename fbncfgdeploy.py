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
from fbnconfig import Deployment, deploy, property

# Set pandas display options
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.options.display.float_format = "{:,.2f}".format

# Initialise environment
secrets_path = os.getenv("FBN_SECRETS_PATH")
if secrets_path is None:
    secrets_path = os.path.join(os.path.dirname(os.getcwd()), "secrets.json")

api_factory = ApiClientFactory(
    token=RefreshingToken(),
    api_secrets_filename=secrets_path,
    app_name="FbnCfgPoc"
)

# Deploy via existing deployment procedure.
import properties
properties.main(api_factory)

# Deploy fbn config
def configure(env):
    # Config item independent to existing configuration - new folder in root directory of drive.
    poc_folder_res = drive.FolderResource(id="folder02", name="POC5_folder", parent=drive.root)

    # Config item dependent to exsting configuration - derived property of existing property.
    # reference for underlying value property
    rating_test_ref = property.DefinitionRef(
        id="Instrument_fbn-cfg-test_RatingTest_01", domain=property.Domain.Instrument, scope="fbn-cfg-test", code="RatingTest"
    )

    normalised_rating_res = property.DefinitionResource(
        id="Instrument_fbn-cfg-test_RatingScoreTest_01",
        domain=property.Domain.Instrument,
        data_type_id=property.ResourceId(scope="system", code="string"),
        scope="fbn-cfg-test",
        code="RatingScoreTest",
        property_description="Normlaise underlying rating",
        display_name="Rating Score Test",
        derivation_formula=property.Formula("coalesce ({x})", x=rating_test_ref),
    )

    return Deployment("my_deployment", [
        normalised_rating_res,
        poc_folder_res
        ]
    )

host_vars = {} # I think this is just dictionary representation of vars file.
lusid_url = os.getenv("LUSID_ENV")
token = api_factory.api_client.configuration.access_token
deployment = configure(host_vars)

deploy(deployment, lusid_url, token)