import csv
import json
from datetime import datetime
from glob import glob
from inspect import currentframe
from os import path, makedirs

from excel2meta_interface.utils import messages, helpers
from excel2meta_interface.excel2json import mapping_source_target_zones


class JSON2EDCLineageFiles:
    code_version = "0.1.0"
    start_time = datetime.now()
    start_time_formatted = start_time.isoformat(timespec="microseconds").replace(":", "-")
    edc_lineage_column_header = [
        "Association",
        "From Connection",
        "To Connection",
        "From Object",
        "To Object",
    ]

    def __init__(self, configuration_file="resources/json2edc_config.json"):
        self.configuration_file = configuration_file
        self.result = messages.message["ok"]
        self.schema_directory = "schemas"
        self.json_directory = "jsons"
        self.output_directory = "out/"
        self.helper = helpers.UtilsHelper()
        self.nr_entity_associations = 0
        self.nr_attribute_associations = 0
        self.excel_file = None
        self.resource_items = None
        self.ref_directory = None
        self.get_settings(configuration_file=configuration_file)
        makedirs(self.output_directory, exist_ok=True)

        self.mapping_ref = mapping_source_target_zones.MappingSource2TargetZone(
            excel_file="mapping_overview_consolidated.xlsx", sheet="Sheet3"
        )

    def process_files(self, excelfile=None):
        module = __name__ + "." + currentframe().f_code.co_name
        if excelfile is not None:
            self.excel_file = excelfile
            self.json_directory += excelfile + "/"

        print("JSON directory:", self.json_directory)
        print("Output directory:", self.output_directory)

        number_of_files = 0
        overall_result = messages.message["ok"]
        for file in glob(self.json_directory + "*.json"):
            number_of_files +=1
            data = self.helper.get_json(file)
            check_result = self.helper.check_schema(base_schema_folder=self.schema_directory, data=data)
            if check_result["code"] != "OK":
                file_result = check_result
                file_result["info"] = "File: %s. Error: %s" % (file, check_result["info"])
                overall_result = file_result
            else:
                file_result = self.process_json_data(data)
                if file_result["code"] != "OK":
                    overall_result = file_result

            # register the outcome of the current file
            self.register_result(file, file_result)

        if overall_result["code"] == "OK":
            overall_result["info"] = \
                "#files processed: >%d<. #entity assocations: >%d<. #attribute assocications: >%d<" \
                % (number_of_files, self.nr_entity_associations, self.nr_attribute_associations)

        return overall_result

    def get_settings(self, configuration_file):
        result = messages.message["ok"]
        try:
            with open(configuration_file) as config:
                data = json.load(config)
                self.schema_directory = data["schema_directory"]
                self.json_directory = data["json_directory"]
                if "output_directory" in data:
                    self.output_directory = path.join(data["output_directory"], self.start_time_formatted)
                else:
                    self.output_directory = path.join(self.output_directory, self.start_time_formatted)
                if self.excel_file is not None:
                    self.json_directory = path.join(self.json_directory, self.excel_file)
                self.resource_items = data["resource_items"]
                if "ref_directory" in data:
                    self.ref_directory = data["ref_directory"]
                else:
                    self.ref_directory = self.output_directory
                # print("resource_items:", self.resource_items)
        except FileNotFoundError or IOError as e:
            result = messages.message["main_config_not_found"]
            result["info"] = "configuration file used: >%s<" % configuration_file
            return result
        return result

    def process_json_data(self, data):
        result = messages.message["ok"]
        if data["meta"] == "physical_entity_association":
            self.nr_entity_associations += 1
            result = self.generate_dataset_lineage_entry(data)
        elif data["meta"] == "physical_attribute_association":
            self.nr_attribute_associations += 1
            result = self.generate_attribute_lineage_entry(data)

        return result

    def generate_dataset_lineage_entry(self, data):
        result = messages.message["ok"]

        for source_target_entity_link in data["source_target_entity_links"]:
            src = source_target_entity_link["from"]
            tgt = source_target_entity_link["to"]
            src_dataset = self.get_dataset(uuid=src)
            if src_dataset is None:
                result = messages.message["entity_uuid_not_found"]
                result["info"] = "source uuid: %s" % src
                return result
            tgt_dataset = self.get_dataset(uuid=tgt)
            if tgt_dataset is None:
                result = messages.message["entity_uuid_not_found"]
                result["info"] = "target uuid: %s" % src
                return result
            item = self.create_dataset_item(source_name=src_dataset["name"], target_name=tgt_dataset["name"])
            self.write_lineage_entry(item)

        return result

    def get_dataset(self, uuid):
        for file in glob(self.json_directory + "*.json"):
            with open(file) as f:
                data = json.load(f)
                if "meta" not in data:
                    continue
                meta = data["meta"]
                if meta == "physical_entity":
                    if data["uid"] == uuid:
                        return data
        return None

    def create_dataset_item(self, source_name, target_name):
        # get info from REF files, generated out of the Excel by excel2references
        src_ref = self.get_dataset_ref("source", source_name)
        if src_ref is None:
            print("Could not find source reference for >%s<" % source_name)
            src_path = "NONE://" + source_name
        else:
            src_edc_datasource, src_prefix, src_layer, src_zone = self.get_datasource_ref(src_ref["src_zone"])
            src_path = src_edc_datasource + "://" + src_prefix + src_ref["src_zone"] + "/" + source_name
        tgt_ref = self.get_dataset_ref("target", target_name)
        if tgt_ref is None:
            print("Could not find target reference for >%s<" % target_name)
            tgt_path = "NONE://" + target_name
        else:
            tgt_edc_datasource, tgt_prefix, tgt_layer, tgt_zone = self.get_datasource_ref(tgt_ref["tgt_zone"])
            if tgt_zone is None or tgt_zone == "":
                tgt_path = tgt_edc_datasource + "://" + tgt_prefix + tgt_layer + "/" + target_name
            else:
                tgt_path = tgt_edc_datasource + "://" + tgt_prefix + tgt_ref["tgt_zone"]  + "/" + target_name

        item = ["core.DataSetDataFlow", "", "", src_path, tgt_path]
        return item

    def get_datasource_ref(self, ref):
        print("get_datasource_ref for >%s<" % ref)
        the_layer = "NO_LAYER"
        the_zone = "NO_ZONE"
        the_datasource = "NONE"
        the_prefix = "FileServer/"
        splits = ref.split("/", 4)
        for split in splits:
            if "_layer" in split:
                the_layer = split
            if "_zone" in split:
                the_zone = split
        for item in self.resource_items:
            if item["layer"] == the_layer:
                the_datasource = item["resource"]
                the_zone = item["zone"]
                the_prefix = item["prefix"]

        print("For ref >%s<: datasource >%s< prefix >%s<, layer >%s<, zone >%s<." % (ref, the_datasource, the_prefix, the_layer, the_zone))

        return the_datasource, the_prefix, the_layer, the_zone

    def get_dataset_ref(self, src_or_tgt, dataset_name):
        file = self.find_latest_ref_file(src_or_tgt)
        if file is None:
            print("Could not find a dataset REF file for >%s< >%s<" % (src_or_tgt, dataset_name))
            return None
        print("Using ref file:", file)
        data = None
        with open(file, "r") as the_file:
            data = json.load(the_file)
        if src_or_tgt == "source":
            for source in data:
                if source["dataset"] == dataset_name:
                    print("found entry for dataset >%s<" % dataset_name, source)
                    return source
        elif src_or_tgt == "target":
            for entry in data:
                if entry["dataset"] == dataset_name:
                    print("found entry for dataset >%s<" % dataset_name, entry)
                    return entry
        else:
            print("Incorrect src_or_tgt:", src_or_tgt)
        print("get_dataset_ref: Could not find reference for >%s< >%s<" % (src_or_tgt, dataset_name))
        return None

    def find_latest_ref_file(self, src_or_tgt):
        search_for_files = self.ref_directory + "/" + "20*--REF_-_data-sources-" + src_or_tgt + "*dataset.json"
        # print("Looking for REF files with search >%s<" % search_for_files)
        list_of_files = glob(search_for_files)
        if list_of_files is not None and len(list_of_files) > 0:
            latest_file = max(list_of_files, key=path.getctime)
        else:
            latest_file = None
        return latest_file

    def generate_attribute_lineage_entry(self, data):
        result = messages.message["ok"]

        entity_association_uuid = data["physical_entity_association"]
        entity_assocation = self.get_entity_association(entity_association_uuid)
        from_entities = self.get_source_entities(entity_assocation)
        to_entities = self.get_target_entities(entity_assocation)

        overall_result = messages.message["ok"]
        nr_link = 0
        for source_target_attribute_link  in data["source_target_attribute_links"]:
            nr_link += 1
            description="none"
            formula="none"
            to_attribute = source_target_attribute_link["transformation"]["to"]
            # to_attribute has to be in one of the target entities
            result_check, entity, to_attribute_name = self.get_entity_attribute(to_entities, to_attribute)
            tgt_entity_uuid = self.get_entity(entity_uuid=entity)
            if tgt_entity_uuid is None:
                result = messages.message["target_entity_not_found"]
                result["info"] = "Could not find entity with uuid >%s< in to_entities >%s<" % (entity, str(to_entities))
                overall_result = result
                continue
            else:
                tgt_entity = tgt_entity_uuid["name"]
            if not result_check:
                result = messages.message["target_attribute_not_in_target_entities"]
                result["info"] = "to_attribute >%s< not found in target entities >%s<" % (to_attribute, str(to_entities))
                overall_result = result
                continue
            if description in source_target_attribute_link:
                description = source_target_attribute_link["description"]
            if formula in source_target_attribute_link:
                formula = source_target_attribute_link["formula"]
            nr_from = 0
            for from_attribute in source_target_attribute_link["transformation"]["from"]:
                nr_from += 1
                # print("from:", from_attribute, "to:", to_attribute)
                # from_attribute has to be in one of the source entities
                result_check, entity, from_attribute_name = self.get_entity_attribute(from_entities, from_attribute)
                if not result_check:
                    result = messages.message["source_attribute_not_in_source_entities"]
                    result["info"] = "from_attribute >%s< (%s) not found in source entities >%s<" \
                                     % (from_attribute, from_attribute_name, str(from_entities))
                    overall_result = result
                else:
                    src_entity = self.get_entity(entity_uuid=entity)["name"]
                    item = self.create_attribute_item(source_dataset=src_entity
                                                      , source_attribute=from_attribute_name
                                                      , target_dataset=tgt_entity
                                                      , target_attribute=to_attribute_name)
                    self.write_lineage_entry(item)

        return overall_result

    def create_attribute_item(self, source_dataset, source_attribute, target_dataset, target_attribute):
        # get info from REF files, generated out of the Excel by excel2references
        src_ref = self.get_dataset_ref("source", source_dataset)
        if src_ref is None:
            print("Could not find source dataset reference for attribute >%s< in source >%s<"
                  % (source_attribute, source_dataset))
            src_path = "NONE://" + source_dataset + "/" + source_attribute
        else:
            src_edc_datasource, src_prefix, src_layer, src_zone = self.get_datasource_ref(src_ref["src_zone"])
            src_path = src_edc_datasource + "://" + src_prefix + src_ref["src_zone"] \
                       + "/" + source_dataset + "/" + source_attribute
        tgt_ref = self.get_dataset_ref("target", target_dataset)
        if tgt_ref is None:
            print("Could not find target dataset reference for attribute >%s< in target >%s<"
                  % (target_attribute, target_dataset))
            tgt_path = "NONE://" + target_dataset + "/" + target_attribute
        else:
            tgt_edc_datasource, tgt_prefix, tgt_layer, tgt_zone = self.get_datasource_ref(tgt_ref["tgt_zone"])
            if tgt_zone is None or tgt_zone == "":
                tgt_path = tgt_edc_datasource + "://" + tgt_prefix + tgt_layer \
                           + "/" + target_dataset + "/" + target_attribute
            else:
                tgt_path = tgt_edc_datasource + "://" + tgt_prefix + tgt_ref["tgt_zone"] \
                           + "/" + target_dataset + "/" + target_attribute

        item = ["core.DirectionalDataFlow", "", "", src_path, tgt_path]
        return item

    def get_entity_attribute(self, entities, attribute):
        """
            Check if the attribute uuid is part of one of the entities in the provided list
        :param entities:
        :param attribute:
        :return:
        """
        print("looking for attribute >%s<" % attribute)
        for entity in entities:
            entity_attributes = self.get_attributes(entity)
            # print("Entity >%s< #attributes >%d<" % (entity, len(entity_attributes)))
            if entity_attributes is None:
                print("Could not determine attributes for entity >%s<" % entity)
            else:
                for entity_attribute in entity_attributes:
                    if entity_attribute["uid"] == attribute:
                        print("Found: entity_attribute >%s< is named >%s<" % (entity_attribute["uid"], entity_attribute["name"]))
                        return True, entity, entity_attribute["name"]
        print("NOT FOUND: attribute >%s< in entity list >%s<" % (attribute, str(entities)))
        return False, None, None

    def get_attributes(self, entity):
        for file in glob(self.json_directory + "*.json"):
            with open(file) as f:
                data = json.load(f)
                if "meta" not in data:
                    continue
                meta = data["meta"]
                if meta == "physical_attribute":
                    if data["physical_entity"] == entity:
                        return data["attribute_list"]
        return None

    def get_entity(self, entity_uuid):
        for file in glob(self.json_directory + "*.json"):
            with open(file) as f:
                data = json.load(f)
                if "meta" not in data:
                    continue
                meta = data["meta"]
                if meta == "physical_entity":
                    if data["uid"] == entity_uuid:
                        return data
        return None

    def get_entity_association(self, entity_assoc_id):
        for file in glob(self.json_directory + "*.json"):
            with open(file) as f:
                data = json.load(f)
                if "meta" not in data:
                    continue
                meta = data["meta"]
                if meta == "physical_entity_association":
                    if data["uid"] == entity_assoc_id:
                        return data
        return None

    def get_source_entities(self, entity_assoc_id):
        sources = []
        for source_target_entity_link in entity_assoc_id["source_target_entity_links"]:
            sources.append(source_target_entity_link["from"])
        return sources

    def get_target_entities(self, entity_assoc_id):
        targets = []
        for source_target_entity_link in entity_assoc_id["source_target_entity_links"]:
            if source_target_entity_link["to"] not in targets:
                targets.append(source_target_entity_link["to"])
        return targets

    def write_lineage_entry(self, entry):
        filename = path.join(self.output_directory, "lineage-" + self.start_time_formatted + ".csv")
        if path.exists(filename):
            append_or_write = "a"
            write_header = False
        else:
            append_or_write = "w"
            write_header = True

        with open(filename, append_or_write) as out:
            col_writer = csv.writer(out)
            if write_header:
                col_writer.writerow(self.edc_lineage_column_header)
            col_writer.writerow(entry)

    def register_result(self, file, result):
        print("Result for file >%s< is >%s<" % (file, result["code"]))
        filename = path.join(self.output_directory, "results-" + self.start_time_formatted + "-" + __name__ + ".txt")
        if path.exists(filename):
            append_or_write = "a"
        else:
            append_or_write = "w"
        with open(filename, append_or_write) as out:
            out.write(file + ": " + json.dumps(result) + "\n")
        if result["code"] != "OK":
            filename = path.join(self.output_directory, "errors-" + self.start_time_formatted + "-" + __name__ + ".txt")
            if path.exists(filename):
                append_or_write = "a"
            else:
                append_or_write = "w"
            with open(filename, append_or_write) as out:
                out.write(file + ": " + json.dumps(result) + "\n")
