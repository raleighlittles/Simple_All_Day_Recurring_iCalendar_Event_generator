import datetime
import icalendar
import os
import socket
import uuid

def get_start_and_end_dates(input_yaml):

    date_format_str = input_yaml["date_fmt_str"]

    start_date_raw, last_possible_date_raw = input_yaml["start_date"], input_yaml["last_possible_date"]

    start_timestamp = datetime.datetime.strptime(start_date_raw, date_format_str)

    start_date = datetime.date(year=start_timestamp.year, month=start_timestamp.month, day=start_timestamp.day)

    last_possible_timestamp = datetime.datetime.strptime(last_possible_date_raw, date_format_str)

    last_possible_date = datetime.date(year=last_possible_timestamp.year, month=last_possible_timestamp.month, day=last_possible_timestamp.day)

    return tuple([start_date, last_possible_date])

def parse_period_from_yaml(input_yaml) -> dict:

    yaml_frequency_key = "frequency"
    days_key_name, weeks_key_name = "days", "weeks"

    unit, duration = "", ""

    days_duration = input_yaml[yaml_frequency_key].get(days_key_name)
    weeks_duration = input_yaml[yaml_frequency_key].get(weeks_key_name)

    if days_duration is not None:
        unit = days_key_name
        duration = days_duration
        
    elif weeks_duration is not None:
        # if not using days, must be using weeks
        unit = weeks_key_name
        duration = weeks_duration

    else:
        raise ValueError("Couldn't parse frequency of events")

    return {"unit": unit, "frequency": int(duration)}


def generate_events_list(first_event_date, last_possible_event_date, time_between_events):

    events = list([first_event_date])

    next_event_date = first_event_date + time_between_events

    if (next_event_date > last_possible_event_date):

        raise ValueError(f"ERROR: Event duration '{time_between_events}' is too short to be used with given last event date '{last_possible_event_date}'. Cannot create list of 1 event")
    
    while (next_event_date < last_possible_event_date):

        events.append(next_event_date)
        next_event_date = next_event_date + time_between_events
    

    print(f"Found {len(events)} events between {first_event_date} and {last_possible_event_date}")
    return events


def create_calendar_obj():

    calendar_obj = icalendar.Calendar()

    # Metadata required by standard
    calendar_obj.add("prodid", f"-//{socket.gethostname()}//NONSGML {os.path.basename(__file__)}//EN")
    calendar_obj.add("version", "2.0")

    return calendar_obj


def get_event_organizer(input_yaml):

    organizer_top_level_key = "organizer"

    organizer = dict()
    organizer = icalendar.vCalAddress(f"MAILTO:{input_yaml[organizer_top_level_key].get('email')}")
    organizer.params["name"] = icalendar.vText(input_yaml[organizer_top_level_key]["name"])

    # Optional fields
    organizer_role = input_yaml[organizer_top_level_key].get("role")
    
    if organizer_role is not None:
        organizer.params["role"] = icalendar.vText(organizer_role)


    return organizer


def add_events_to_calendar(calendar_obj, events_list, event_metadata):

    print(f"[DEBUG] Adding {len(events_list)} events to calendar")

    event_name_key = "common_description"

    # assume organizer of all events is the same
    event_organizer = get_event_organizer(event_metadata)

    for event_idx, event_datetime in enumerate(events_list):

        event_obj = icalendar.Event()
        
        event_obj.add("name", f"{event_metadata[event_name_key]} ({event_idx} of {len(events_list)} )")

        # All-day events cannot have a start time associated with them, hence the date
        # instead of the datetime object
        event_obj.add("dtstart", datetime.date(year = event_datetime.year, month = event_datetime.month, day = event_datetime.day))

        event_obj["organizer"] = event_organizer
        event_obj.add("priority", event_metadata["priority"])
        event_obj["location"] = event_metadata["location"]
        event_obj["class"] = event_metadata["class"]
        event_obj["uid"] = uuid.uuid4()

        calendar_obj.add_component(event_obj)

    return calendar_obj


def save_calendar_to_file(calendar_obj, file_location):

    if os.path.exists(file_location):
        raise FileExistsError(f"[ERROR] Can't save calendar to '{file_location}' as this file already exists")
    
    with open(file=file_location, mode="wb") as calendar_file:
        calendar_file.write(calendar_obj.to_ical())

    print(f"[DEBUG] Finished writing calendar file to '{file_location}' ({os.path.getsize(file_location)} bytes)")