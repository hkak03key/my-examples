from flask import escape

import os
from pprint import pprint
from datetime import datetime, timedelta, timezone

import google_cloud_platform as gcp


PAGINATE_QUEUE_PATH = os.environ.get("PAGINATE_QUEUE_PATH")

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

    is_paginate = True if request_json.get("is_paginate") == True else False
    print("is_paginate:", is_paginate)

    if is_paginate:
        res = gcp.create_pagenate_task(
            PAGINATE_QUEUE_PATH,
            (datetime.now(timezone.utc) + timedelta(minutes=1)).isoformat()
        )

    return escape("complated")

