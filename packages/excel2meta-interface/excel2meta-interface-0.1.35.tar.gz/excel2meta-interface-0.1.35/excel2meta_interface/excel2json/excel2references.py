import csv
import json
from os import path, makedirs
from os.path import basename
from datetime import datetime
from resources import excel_headers
from excel2meta_interface.utils import messages, excel


class Excel2Reference:
    start_time = datetime.now()

    def __init__(self, configuration_file="resources/excel2json_config.json"):
        self.excel_location = "resources/datalineage/tmp/excels"
        self.excel_sheet = "excel_file format"
        self.json_directory = "out/"
        self.json_file_prefix = "generated_"
        self.result = messages.message["ok"]
        self.work_book = None
        self.work_sheet = None
        self.excel_utils = excel.Excel()

        try:
            with open(configuration_file) as config:
                data = json.load(config)
                self.excel_location = data["excel_location"]
                self.excel_sheet = data["excel_sheet"]
                if "json_directory" in data:
                    self.json_directory = data["json_directory"]
                if "json_file_prefix" in data:
                    self.json_file_prefix = data["json_file_prefix"]
                else:
                    self.json_file_prefix = self.start_time.isoformat(timespec="microseconds").replace(':', '-')
                if self.json_file_prefix == "TIMESTAMP":
                    self.json_file_prefix = self.start_time.isoformat(timespec="microseconds").replace(':', '-')
                self.json_file_prefix += "--"
        except FileNotFoundError:
            print("Configuration file >" + configuration_file + "< not found.")
            self.result = messages.message["main_config_not_found"]

    def create_output_files(self):
        overall_result = messages.message["ok"]
        info_datasets = []
        # list of source zones
        source_zone_column = excel_headers.source_zone
        source_zones = self.get_distinct(source_zone_column)
        result = self.out_distinct("REF_-_zones-source" + source_zone_column, source_zones)
        if result["code"] != "OK":
            overall_result = result

        # list of target zones
        target_zone_column = excel_headers.target_zone
        target_zones = self.get_distinct(target_zone_column)
        result = self.out_distinct("REF_-_zones-target" + target_zone_column, target_zones)
        if result["code"] != "OK":
            overall_result = result

        # source dataset list
        source_dataset_column = excel_headers.source_dataset_name
        source_datasets = self.get_distinct(source_dataset_column)
        # get additional info
        info_source_datasets = self.get_dataset_info(source_datasets, "dataset")
        print("dataset info collected for >%d< source datasets" % len(info_source_datasets))
        info_datasets.extend(info_source_datasets)
        result = self.out_distinct_combined("REF_-_data-sources-source" + source_dataset_column, info_source_datasets)
        if result["code"] != "OK":
            overall_result = result

        # target dataset list
        target_dataset_column = excel_headers.target_dataset_name
        target_datasets = self.get_distinct(target_dataset_column)
        # get additional info
        info_target_datasets = self.get_dataset_info(target_datasets, "tgtdataset")
        print("dataset info collected for >%d< target datasets" % len(info_target_datasets))
        info_datasets.extend(info_target_datasets)
        print("In total: dataset info collected for >%d< datasets" % len(info_datasets))
        result = self.out_distinct_combined("REF_-_data-sources-target" + target_dataset_column, info_target_datasets)
        if result["code"] != "OK":
            overall_result = result

        # which source zone has which target zone
        src_zone, row = self.search_value_in_row_index(search_string=source_zone_column, row=1)
        tgt_zone, row = self.search_value_in_row_index(search_string=target_zone_column, row=1)
        src_tgt_zones = self.get_distinct_combined(src_zone, tgt_zone)
        result = self.out_distinct_combined("MAP_-_zones-source2target"
                                            + source_zone_column + '_' + target_zone_column, src_tgt_zones)
        if result["code"] != "OK":
            overall_result = result

        # which source dataset in which source zone has which target dataset in which target zone
        src_zone, row = self.search_value_in_row_index(search_string=source_zone_column, row=1)
        tgt_zone, row = self.search_value_in_row_index(search_string=target_zone_column, row=1)
        src_dataset, row = self.search_value_in_row_index(search_string=source_dataset_column, row=1)
        tgt_dataset, row = self.search_value_in_row_index(search_string=target_dataset_column, row=1)
        src_tgt_zones_datasets = self.get_distinct_combined(source_zone=src_zone
                                                            , target_zone=tgt_zone
                                                            , source_dataset=src_dataset
                                                            , target_dataset=tgt_dataset
                                                            )
        result = self.out_distinct_combined("MAP_-_data-sources-source2target"
                                            + source_zone_column + "." + source_dataset_column
                                            + "_" + target_zone_column + "." + target_dataset_column
                                            , src_tgt_zones_datasets)
        if result["code"] != "OK":
            overall_result = result

        for dataset in info_datasets:
            entities = []
            attributes = self.get_dataset_attributes(dataset_info=dataset)
            entity = dict(is_source=dataset["is_source"]
                          , dataset=dataset["dataset"]
                          , src_zone=dataset["src_zone"]
                          , attributes=attributes)
            entities.append(entity)
            file_name = path.join(self.json_directory, self.json_file_prefix + "ATTRIB_-_" + dataset["dataset"])
            self.write_dict_to_file(out_file=file_name, result_list=entities)

        return overall_result

    def get_dataset_attributes(self, dataset_info):
        # print(dataset_info)
        src_dataset_column = self.search_value_in_row_index(
            search_string=excel_headers.source_dataset_name)[0]
        src_attribute_column = self.search_value_in_row_index(
            search_string=excel_headers.source_attribute)[0]
        src_attribute_description = self.search_value_in_row_index(
            search_string=excel_headers.source_attribute_description)[0]
        tgt_dataset_column = self.search_value_in_row_index(
            search_string=excel_headers.target_dataset_name)[0]
        tgt_attribute_column = self.search_value_in_row_index(
            search_string=excel_headers.target_attribute)[0]
        tgt_attribute_description = self.search_value_in_row_index(
            search_string=excel_headers.target_attribute_description)[0]
        if dataset_info["is_source"] == "True":
            attributes = self.search_value_in_column_index(search_string=dataset_info["dataset"]
                                                           , column=src_dataset_column
                                                           , give_column=src_attribute_column
                                                           , give_column2=src_attribute_description
                                                           , name_column1="attribute_name"
                                                           , name_column2="attribute_description"
                                                           , give_list=True)
        else:
            # print("not is_source. search_string >%s< for column >%d<. Asked for >%d< and >%d<."
            #      % (dataset_info["dataset"], tgt_dataset_column, tgt_attribute_column, tgt_attribute_description))
            attributes = self.search_value_in_column_index(search_string=dataset_info["dataset"]
                                                           , column=tgt_dataset_column
                                                           , give_column=tgt_attribute_column
                                                           , give_column2=tgt_attribute_description
                                                           , name_column1="attribute_name"
                                                           , name_column2="attribute_description"
                                                           , give_list=True)
        # print("attributes:", attributes)
        return attributes

    def get_dataset_info(self, datasets, source_or_target):
        info_datasets = []
        # print("source_or_target is:", source_or_target)
        ds_column = self.search_value_in_row_index(search_string=source_or_target)[0]
        description_column = self.search_value_in_row_index(search_string=excel_headers.source_dataset_description)[0]
        id_column = self.search_value_in_row_index(search_string=excel_headers.source_identifier)[0]
        app_column = self.search_value_in_row_index(search_string=excel_headers.application_identifier)[0]
        src_zone_column = self.search_value_in_row_index(search_string=excel_headers.source_zone)[0]
        tgt_zone_column = self.search_value_in_row_index(search_string=excel_headers.target_zone)[0]

        for dataset in datasets:
            description = self.search_value_in_column_index(search_string=dataset, column=ds_column
                                                            , give_column=description_column)
            if description is None:
                description = ""
            the_id = self.search_value_in_column_index(search_string=dataset, column=ds_column
                                                       , give_column=id_column)
            if the_id is None:
                the_id = ""
            the_id = str(the_id)
            app = self.search_value_in_column_index(search_string=dataset, column=ds_column
                                                    , give_column=app_column)
            if app is None:
                app = ""

            is_source = "False"
            if source_or_target == "dataset":
                source_zone = self.search_value_in_column_index(search_string=dataset, column=ds_column
                                                                , give_column=src_zone_column)
                is_source = "True"
            else:
                source_zone = ""
            if source_zone is None:
                source_zone = ""

            if source_or_target == "tgtdataset":
                target_zone = self.search_value_in_column_index(search_string=dataset, column=ds_column
                                                                , give_column=tgt_zone_column)
                is_source = "False"
            else:
                target_zone = ""
            if target_zone is None:
                target_zone = ""

            info_datasets.append(dict(is_source=is_source, dataset=dataset, description=description, id=the_id, app=app
                                      , src_zone=source_zone, tgt_zone=target_zone))

        return info_datasets

    def get_distinct_combined(self, source_zone=None, target_zone=None, source_dataset=None, target_dataset=None):
        if source_zone is None or target_zone is None:
            return None
        if source_dataset is not None and target_dataset is None:
            return None
        if source_dataset is None and target_dataset is not None:
            return None

        values = []
        id_column = self.search_value_in_row_index(search_string=excel_headers.source_identifier)[0]
        app_column = self.search_value_in_row_index(search_string=excel_headers.application_identifier)[0]
        src_zone_column = self.search_value_in_row_index(search_string=excel_headers.source_zone)[0]
        tgt_zone_column = self.search_value_in_row_index(search_string=excel_headers.target_zone)[0]

        for i in range(2, self.work_sheet.max_row + 1):
            source_value = self.work_sheet.cell(row=i, column=source_zone).value
            target_value = self.work_sheet.cell(row=i, column=target_zone).value
            if source_dataset is None:
                combined = dict(source=source_value, target=target_value)
                combined_for_list = combined
                if combined in values:
                    pass
                else:
                    if combined_for_list["target"] is not None:
                        values.append(combined_for_list)
            else:
                source_dataset_value = self.work_sheet.cell(row=i, column=source_dataset).value
                target_dataset_value = self.work_sheet.cell(row=i, column=target_dataset).value
                src_zone_excel = self.work_sheet.cell(row=i, column=src_zone_column).value
                if src_zone_excel is not None:
                    src_layer, src_zone, src_area, src_system = self.split_zone_excel_value(src_zone_excel)
                else:
                    src_layer = None
                    src_zone = None
                    src_area = None
                    src_system = None
                tgt_zone_excel = self.work_sheet.cell(row=i, column=tgt_zone_column).value
                if tgt_zone_excel is not None:
                    tgt_layer, tgt_zone, tgt_area, tgt_system = self.split_zone_excel_value(tgt_zone_excel)
                else:
                    tgt_layer = None
                    tgt_zone = None
                    tgt_area = None
                    tgt_system = None
                # combined = dict(source=source_value
                #                , source_dataset=source_dataset_value
                #                , target=target_value
                #                , target_dataset=target_dataset_value
                #                , src_zone=src_zone
                #                , tgt_zone=tgt_zone
                #                )
                combined = dict(
                    source=source_value
                    , source_dataset=source_dataset_value
                    , target=target_value
                    , target_dataset=target_dataset_value
                    , application_id=self.work_sheet.cell(row=i, column=app_column).value
                    , dataset_id=str(self.work_sheet.cell(row=i, column=id_column).value)
                    , src_layer=src_layer
                    , src_zone=src_zone
                    , src_area=src_area
                    , src_system=src_system
                    , tgt_layer=tgt_layer
                    , tgt_zone=tgt_zone
                    , tgt_area=tgt_area
                    , tgt_system=tgt_system
                )
                if combined in values:
                    pass
                else:
                    if combined["target"] is not None and combined["tgt_zone"] is not None:
                        values.append(combined)
        return values

    def split_zone_excel_value(self, zone_from_excel):
        layer = "unknown"
        zone = "unknown"
        area = "unknown"
        system = "unknown"

        fields = zone_from_excel.split('/', 4)
        for field in fields:
            if "_layer" in field.lower():
                layer = field
            if "_zone" in field.lower():
                zone = field
        if len(fields) >= 3:
            area = fields[2]
        if len(fields) >= 4:
            system = fields[3]

        return layer, zone, area, system

    def out_distinct(self, column_name=None, result_list=None):
        if column_name is None or result_list is None:
            return None
        # print(result_list)
        out_file = path.join(self.json_directory, self.json_file_prefix + column_name + ".csv")
        return self.write_list_to_file(out_file, result_list)

    def out_distinct_combined(self, filename, source_targets=None):
        if source_targets is None:
            return 6
        # print(source_targets)
        # method will add extension
        out_file = path.join(self.json_directory, self.json_file_prefix + filename)
        return self.write_dict_to_file(out_file, source_targets)

    def get_distinct(self, column_name=None):
        if column_name is None:
            return None
        values = []

        column, row = self.search_value_in_row_index(search_string=column_name, row=1)

        for i in range(2, self.work_sheet.max_row + 1):
            if self.work_sheet.cell(row=i, column=column).value in values:
                pass
            else:
                if self.work_sheet.cell(row=i, column=column).value is not None:
                    values.append(self.work_sheet.cell(row=i, column=column).value)
        return values

    def search_value_in_row_index(self, search_string, row=1):
        return self.excel_utils.search_value_in_row_index(work_sheet=self.work_sheet, search_string=search_string,
                                                          row=row)

    def search_value_in_column_index(self, search_string, column, give_column, give_column2=None,
                                     name_column1=None, name_column2=None, give_list=False):
        # TODO: Make more generic and flexible
        # Note: give_column2 is only valid in combination with give_list=True

        # print("Searching for", search_string, "in column", column)
        values = []
        for row in self.work_sheet.iter_rows(column):
            for cell in row:
                # print(cell.row, cell.column, cell.value)
                if cell.value == search_string:
                    # print(cell.value)
                    if not give_list:
                        # we found it and we should not provide an entire list, so return to caller
                        return str(self.work_sheet.cell(row=cell.row, column=give_column).value).replace('"',
                                                                                                         '\"').replace(
                            '\\n', ' ')
                    else:
                        if give_column2 is None:
                            value = self.work_sheet.cell(row=cell.row, column=give_column).value
                            if value is None:
                                value = ""
                            else:
                                value = value.replace('"', '\"')
                            values.append(value)
                        else:
                            value1 = self.work_sheet.cell(row=cell.row, column=give_column).value
                            if value1 is None:
                                value1 = ""
                            else:
                                value1 = value1.replace('"', '\"')
                            value2 = self.work_sheet.cell(row=cell.row, column=give_column2).value
                            if value2 is None:
                                value2 = ""
                            else:
                                value2 = value2.replace('"', '\"')
                            col_dict = {name_column1: value1
                                , name_column2: value2}
                            values.append(col_dict)
        if give_list:
            nr = 0
            out_list = []
            for value in values:
                already_exists = False
                for out in out_list:
                    if value["attribute_name"].lower() == out["attribute_name"].lower():
                        already_exists = True
                        break
                if already_exists:
                    pass
                else:
                    out_list.append(value)
            return out_list
        #    return list(set(values))
        else:
            return None

    def write_list_to_file(self, out_file, result_list):
        try:
            with open(out_file, "w", encoding="utf-8", newline='') as csv_file:
                for item in result_list:
                    if item is not None:
                        csv_file.write(item.replace('/', ';') + "\n")
        except IOError:
            print("Error creating or writing to output file >" + out_file + "<.")
            return messages.message["write_error"]
        return messages.message["ok"]

    def write_dict_to_file(self, out_file, result_list):
        result = messages.message["ok"]
        # csv
        file_name = out_file + ".csv"
        try:
            print(result_list)
            if len(result_list) > 0:
                keys = result_list[0].keys()
                with open(file_name, "w", encoding="utf8", newline='') as csv_file:
                    dict_writer = csv.DictWriter(csv_file, keys, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                    dict_writer.writeheader()
                    dict_writer.writerows(result_list)
            else:
                print("Empty result list. Output file >%s< not created" % (out_file + ".csv"))
        except IOError:
            result = messages.message["write_error"]
            result["info"] = "Error creating or writing dictionary to csv output file >" + file_name + "<."
            return result
        # json
        file_name = out_file + ".json"
        try:
            with open(file_name, "w", encoding="utf8", newline='') as json_file:
                json_file.write(json.dumps(result_list, indent=4))
        except IOError:
            result = messages.message["write_error"]
            result["info"] = "Error creating or writing dictionary to json output file >" + file_name + "<."
            print(result["info"])

        return result

    def main(self, excel_file=None, excel_sheet=None):
        if self.result["code"] != "OK":
            return self.result
        if excel_sheet is not None:
            self.excel_sheet = excel_sheet
        self.json_directory += basename(excel_file)
        makedirs(self.json_directory, exist_ok=True)
        print(self.json_directory)
        result, self.work_book, self.work_sheet = self.excel_utils.read_excel(file=excel_file, sheet=self.excel_sheet)
        if result["code"] != "OK":
            return result

        result = self.create_output_files()
        return result


if __name__ == "__main__":
    excel2ref = Excel2Reference(configuration_file="resources/excel2json_config.json")
    result = excel2ref.main(excel_file="tryout.xlsx")
    print("result:", result)
    if result["code"] != "OK":
        exit(1)
    else:
        exit(0)
