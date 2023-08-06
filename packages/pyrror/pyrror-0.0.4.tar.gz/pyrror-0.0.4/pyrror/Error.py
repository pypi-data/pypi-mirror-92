import datetime
import json
import os
import traceback
import requests


class Error:

    def __init__(self, client_id, monitoring_error_url):
        self.client_id = client_id
        self.monitoring_error_url = monitoring_error_url

    def log(self, function_name, error=None):
        body = {
            "client_id": self.client_id,
            "timestamp": str(datetime.datetime.now()),
            "local_absolute_path": os.getcwd(),
            "function_name": function_name,
            "error": traceback.format_exc() if error is None else error
        }
        r = requests.post(url=self.monitoring_error_url, data=json.dumps(body))
        return r.status_code

    def log_error(self, function_name, error):
        body = {
            "client_id": self.client_id,
            "timestamp": str(datetime.datetime.now()),
            "local_absolute_path": os.getcwd(),
            "function_name": function_name,
            "error": error
        }
        r = requests.post(url=self.monitoring_error_url, data=json.dumps(body))
        return r.status_code
