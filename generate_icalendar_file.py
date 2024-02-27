
import argparse
import datetime
import yaml

# locals
import calendar_helper

if __name__ == "__main__":

    argparse_parser = argparse.ArgumentParser()

    argparse_parser.add_argument(
        "-i", "--input-yaml-file", type=str, required=True, help="The input YAML file containing")

    argparse_args = argparse_parser.parse_args()

    input_yaml_filename = argparse_args.input_yaml_file

    with open(input_yaml_filename, mode='r', encoding="utf-8") as input_yaml_file:

        input_yaml = yaml.safe_load(input_yaml_file)

        start_date, last_possible_date = calendar_helper.get_start_and_end_dates(
            input_yaml)

        event_frequency_and_units = calendar_helper.parse_period_from_yaml(
            input_yaml)

        units, frequency = event_frequency_and_units["unit"], event_frequency_and_units["frequency"]

        period = None

        if units == "weeks":
            period = datetime.timedelta(weeks=frequency)

        elif units == "days":
            period = datetime.timedelta(days=frequency)

        events_list = calendar_helper.generate_events_list(
            start_date, last_possible_date, period)

        calendar_obj = calendar_helper.create_calendar_obj()

        calendar_obj_with_events = calendar_helper.add_events_to_calendar(
            calendar_obj, events_list, input_yaml)

        calendar_helper.save_calendar_to_file(
            calendar_obj_with_events, input_yaml["output_filename"])
