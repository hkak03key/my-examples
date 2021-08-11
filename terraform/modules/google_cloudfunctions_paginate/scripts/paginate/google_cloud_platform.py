import json
import os
import re
import requests

import google.auth
from google.cloud import tasks_v2 as tasks
from google.protobuf import timestamp_pb2



def get_self_service_account_email():
    response = requests.get(
        "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email",
        headers={"Metadata-Flavor": "Google"}
    )
    return response.text


def get_self_project_id():
    _, project_id = google.auth.default()
    return project_id


def get_self_region():
    response = requests.get("http://metadata.google.internal/computeMetadata/v1/instance/zone",
    headers={"Metadata-Flavor": "Google"})

    re_search = re.search(r"projects/(?P<project_num>[0-9]+)/zones/(?P<zone>.+)", response.text)
    zone = re_search.group("zone")

    re_search = re.search(r"^(?P<region>[a-zA-Z]+-[a-zA-Z0-9]+)", zone)
    region = re_search.group("region")
    return region


def get_self_function_name():
    function_name = os.environ.get("K_SERVICE")
    if not function_name:
        function_name = os.environ.get("FUNCTION_NAME")
    return function_name


def get_self_url():
    if os.environ.get("FUNCTION_SIGNATURE_TYPE") != "http":
        return None

    project_id = get_self_project_id()
    if not project_id:
        return None

    region = get_self_region()
    if not region:
        return None

    function_name = get_self_function_name()
    if not function_name:
        return None

    return "https://{}-{}.cloudfunctions.net/{}".format(region, project_id, function_name)


def create_pagenate_task(target_queue_path, schedule_time_str, body={}):
    client = tasks.CloudTasksClient()

    schedule_time_pb2 = timestamp_pb2.Timestamp()
    schedule_time_pb2.FromJsonString(schedule_time_str) # FromJsonString()の戻り値はNone

    task = {
        "name": "{}/tasks/{}_paginate_{}".format(target_queue_path, get_self_function_name(), re.sub(r"\D", "", schedule_time_str)),
        "schedule_time": schedule_time_pb2,
        "http_request": {  # Specify the type of request.
            "http_method": "POST",
            "url": get_self_url(),
            "oidc_token": {
                "service_account_email": get_self_service_account_email(),
            },
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps(body).encode(),
        },
    }

    response = client.create_task(request={"parent": target_queue_path, "task": task})

    print("Created task {}".format(response.name))
    return response

