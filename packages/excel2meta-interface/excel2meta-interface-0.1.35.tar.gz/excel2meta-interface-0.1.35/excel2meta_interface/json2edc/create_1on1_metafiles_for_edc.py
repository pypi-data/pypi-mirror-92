from excel2meta_interface.utils import messages
# import informatica_edc_rest_api_samples
from edc_rest_api.metadata_utilities import load_json_metadata
import glob


class CreateOneOnOneMetafilesForEDC:
    def __init__(self):
        self.result = messages.message["ok"]
        self.config_directory = "lineage_output/one-on-one/config/"

    def create_metafiles(self):
        print("Creation of metadata files with config files in >%s<" % self.config_directory)
        for file in glob.glob(self.config_directory + "config_for_*.json"):
            print("Processing with configuration file >%s<" % file)
            load_json = load_json_metadata.ConvertJSONtoEDCLineage(configuration_file=file)
            return load_json.main(metafiles_only=True)


if __name__ == "__main__":
    result = CreateOneOnOneMetafilesForEDC().create_metafiles()
    print(result)
    if result["code"] == "OK":
        exit(0)
    else:
        exit(1)
