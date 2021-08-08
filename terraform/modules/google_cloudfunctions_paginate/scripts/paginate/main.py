from flask import escape

import os
from pprint import pprint
from datetime import datetime, timedelta, timezone

import google_cloud_platform as gcp

def main(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    pprint({"request_json": request_json})

    is_final = False if not request_json.get("is_final") else True
    print("is_final:", is_final)

    if not is_final:
        res = gcp.create_pagenate_task(
            (datetime.utcnow() + timedelta(minutes=1)).isoformat()
        )
    pprint(res)

    return escape("complated")

