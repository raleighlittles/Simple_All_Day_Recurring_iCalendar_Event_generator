# About / Background

This is a very simple script for creating an iCalendar file based on a set of fixed-period events, e.g. biweekly paychecks, 9/80 schedules.

Use the `rules.yaml` file to specify some info about the event sequence, such as:

* the start date
* the end date
* the period of events, in either weeks or days
* a common name for the events, used in each event's title (which are automatically numbered)

You can also set additional metadata for the events, like an organizer, a location, and a priority.

For more information on iCalendar files, read [RFC 5545](https://www.rfc-editor.org/rfc/rfc5545)

# Usage

First install dependencies:

```bash
$ pip install -r requirements.txt
```

Usage info:

```
usage: generate_icalendar_file.py [-h] -i INPUT_YAML_FILE

options:
  -h, --help            show this help message and exit
  -i INPUT_YAML_FILE, --input-yaml-file INPUT_YAML_FILE
                        The input YAML file containing

```