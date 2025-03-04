# Set up LUSID
import os
import pandas as pd
import json
import json

import logging
logging.basicConfig(level=logging.INFO)

import lusid as lu
import lusid.api as la
import lusid.models as lm
import lusid.exceptions as le

from lusid.utilities import ApiClientFactory
from lusidjam import RefreshingToken

config_file = 'properties.csv'

def main(api_factory):
    properties_df = pd.read_csv(config_file)
    print(properties_df.to_string())

    # Build api
    lusid_properties_api = api_factory.build(la.PropertyDefinitionsApi)

    # Create each property with a different call to api.
    for index, property_def in properties_df.iterrows():

        try:
            create_reponse = lusid_properties_api.create_property_definition(
                lm.CreatePropertyDefinitionRequest(
                    domain = property_def["domain"],
                    scope = property_def["scope"],
                    code = property_def["code"],
                    display_name = property_def["code"],
                    data_type_id = lm.ResourceId(
                        scope = "system",
                        code = "string"
                    ),
                    property_description = property_def["code"],
                )
            )

            logging.info(f'Successfully addes property def for {property_def["domain"]}/{property_def["scope"]}/{property_def["code"]}')
        
        except le.ApiException as ex:

            if json.loads(ex.body)['code'] == 124:
                logging.info(f'Property {property_def["domain"]}/{property_def["scope"]}/{property_def["code"]} already exists, delete and recreate.')

                lusid_properties_api.delete_property_definition(
                    domain = property_def["domain"],
                    scope = property_def["scope"],
                    code = property_def["code"]
                )

                lusid_properties_api.create_property_definition(
                    lm.CreatePropertyDefinitionRequest(
                        domain = property_def["domain"],
                        scope = property_def["scope"],
                        code = property_def["code"],
                        display_name = property_def["code"],
                        data_type_id = lm.ResourceId(
                            scope = "system",
                            code = "string"
                        ),
                        property_description = property_def["code"],
                    )
                )

                logging.info(f'Property {property_def["domain"]}/{property_def["scope"]}/{property_def["code"]} successfully recreated.')

            else:
                raise

if __name__ == "__main__":
    # Set pandas display options
    pd.set_option("display.max_columns", None)
    pd.set_option("display.max_rows", None)
    pd.options.display.float_format = "{:,.2f}".format

    secrets_path = os.getenv("FBN_SECRETS_PATH")

    # Run the Notebook locally using a secrets file (see https://support.lusid.com/knowledgebase/article/KA-01663)
    if secrets_path is None:
        secrets_path = os.path.join(os.path.dirname(os.getcwd()), "secrets.json")

    api_factory = ApiClientFactory(
        token=RefreshingToken(),
        api_secrets_filename=secrets_path,
        app_name="Test properties deployment"
    )

    logging.info(f'LUSID Environment Initialised')
    logging.info(f'API Version: {api_factory.build(la.ApplicationMetadataApi).get_lusid_versions().build_version}')

    main(api_factory)