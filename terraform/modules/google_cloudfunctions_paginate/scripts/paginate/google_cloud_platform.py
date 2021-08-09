import os
from datetime import datetime
import json

import google.auth
from google.cloud import tasks_v2 as tasks
from google.protobuf import timestamp_pb2


_, PROJECT_ID = google.auth.default()

FUNCTION_REGION = os.environ.get("FUNCTION_REGION")

FUNCTION_NAME = os.environ.get("K_SERVICE")
if not FUNCTION_NAME:
    FUNCTION_NAME = os.environ.get("FUNCTION_NAME")


def get_self_url():
    if os.environ.get("FUNCTION_SIGNATURE_TYPE") != "http":
        return None

    if not PROJECT_ID:
        return None

    if not FUNCTION_REGION:
        return None

    if not FUNCTION_NAME:
        return None

    return "https://{}-{}.cloudfunctions.net/{}".format(FUNCTION_REGION, PROJECT_ID, FUNCTION_NAME)


def create_pagenate_task(schedule_datetime_str, function_invoker):
    client = tasks.CloudTasksClient()

    queue = FUNCTION_NAME
    parent = client.queue_path(PROJECT_ID, FUNCTION_REGION, queue)

    schedule_datetime = datetime.fromisoformat(schedule_datetime_str)

    task = {
        "name": "{}/tasks/{}_paginate_{}".format(parent, FUNCTION_NAME, int(schedule_datetime.timestamp())),
        "schedule_time": timestamp_pb2 \
                .Timestamp() \
                .FromDatetime(
                    schedule_datetime
                ),
        "http_request": {  # Specify the type of request.
            "http_method": "POST",
            "url": get_self_url(),
            "oidc_token": {
                "service_account_email": function_invoker,
            },
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps({
                "is_paginate": False,
            }).encode(),
        },
    }

    response = client.create_task(request={"parent": parent, "task": task})

    print("Created task {}".format(response.name))
    return response

