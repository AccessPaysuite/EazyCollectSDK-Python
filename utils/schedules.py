from pathlib import Path
from datetime import datetime
from ..settings import other
from ..settings import current_environment
import json
from ..get import Get


base_path = Path(__file__).parent
sandbox_schedules_file = (base_path / '../includes/sandbox.csv').resolve()
ecm3_schedules_file = (base_path / '../includes/ecm3.csv').resolve()


def read_available_schedules_file():
    # Check the current environment, and select the appropriate file
    if current_environment['env'] == 'sandbox':
        file = sandbox_schedules_file
    else:
        file = ecm3_schedules_file
    # Instantiate the dictionary we will parse JSON into
    schedules_json = {}
    date_today = datetime.now().date()
    day_difference = 0

    with open(file, 'a+') as f:
        f.seek(0)
        try:
            data = json.load(f)
            # ISO date formatting
            date_format = '%Y-%m-%d'
            last_update_date_text = data['last_update_date']['last_updated']
            last_update_date = datetime.strptime(
                last_update_date_text,
                date_format,
            )
            day_difference += date_today.day - last_update_date.day

            # Instantiate the JSON object to be written to
            schedules_json['schedule'] = []
            # Get the schedules from ECM3
            schedules = Get.schedules()
            services_list = json.loads(schedules)
            # Read the schedules
            schedule_list = services_list['Services']

            for i in range(len(schedule_list)):
                schedules = (schedule_list[i]['Schedules'])
                for schedule in schedules:
                    # Ad-hoc will appear nowhere else other than
                    # potentially name. It will be in Description
                    # every time, however.
                    if 'AD-HOC Payments' in schedule['Description']:
                        schedule_type = False
                    else:
                        schedule_type = True

                    schedules_json['schedule'].append({
                        'name': schedule['Name'],
                        'ad_hoc': schedule_type,
                        'frequency': schedule['Frequency'],
                    })
                    # We save the date in ISO format, but JSON cannot
                    # parse a date
                schedules_json['last_update_date'] = ({
                    'last_updated': str(datetime.now().date())
                })
            if day_difference >= 365 or other['force_schedule_updates']:
                update_schedules_file(schedules_json)

            return schedules_json

        except:
            # Instantiate the JSON object to be written to
            schedules_json['schedule'] = []
            # Get the schedules from ECM3
            schedules = Get.schedules()
            services_list = json.loads(schedules)
            # Read the schedules
            schedule_list = services_list['Services']

            for i in range(len(schedule_list)):
                schedules = (schedule_list[i]['Schedules'])
                for schedule in schedules:
                    # Ad-hoc will appear nowhere else other than
                    # potentially name. It will be in Description
                    # every time, however.
                    if 'AD-HOC Payments' in schedule['Description']:
                        schedule_type = False
                    else:
                        schedule_type = True

                    schedules_json['schedule'].append({
                        'name': schedule['Name'],
                        'ad_hoc': schedule_type,
                        'frequency': schedule['Frequency'],
                    })
                    # We save the date in ISO format, but JSON cannot
                    # parse a date
                schedules_json['last_update_date'] = ({
                    'last_updated': str(datetime.now().date())
                })
            update_schedules_file(schedules_json)
            return schedules_json


def update_schedules_file(schedules_json):
    if current_environment['env'] == 'sandbox':
        file = sandbox_schedules_file
    else:
        file = ecm3_schedules_file

    with open(file, 'w') as f:
        json.dump(schedules_json, f)
    return 'Updated bank holidays file.'
