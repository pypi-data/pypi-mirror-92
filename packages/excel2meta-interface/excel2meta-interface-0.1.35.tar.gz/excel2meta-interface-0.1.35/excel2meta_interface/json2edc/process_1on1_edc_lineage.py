import glob
from datetime import datetime

# import informatica_edc_rest_api_samples
from edc_rest_api.metadata_utilities import load_json_metadata

from excel2meta_interface.utils import messages


class ProcessOneOnOneLineageEDC:
    def __init__(self, configuration_directory="lineage_output/one-on-one/config/"):
        self.result = messages.message["ok"]
        self.config_directory = configuration_directory

    def upload_lineage(self):
        overall_result = messages.message["ok"]
        print("Uploading lineage to EDC with config files in >%s<" % self.config_directory)
        for file in glob.glob(self.config_directory + "config_for_*.json"):
            print("=== START === Lineage processing with configuration file >%s<" % file)
            start_time = datetime.now()
            load_json = load_json_metadata.ConvertJSONtoEDCLineage(configuration_file=file)
            result = load_json.process_files(ignore_metafile_creation=True)
            end_time = datetime.now()
            run_time = datetime.now() - start_time
            # print(result)
            print("%s - file >%s< processing time was >%s<. Result is >%s< - >%s<" % (
            end_time.isoformat(timespec="microseconds")
            , file
            , str(run_time)
            , result["code"]
            , result["message"]))
            if result["code"] != "OK":
                overall_result = result
        return overall_result


if __name__ == "__main__":
    ProcessOneOnOneLineageEDC().upload_lineage()
