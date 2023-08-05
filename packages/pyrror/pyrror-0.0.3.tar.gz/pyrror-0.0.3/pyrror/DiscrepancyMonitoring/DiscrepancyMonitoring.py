import requests

from pyrror.DiscrepancyMonitoring.analyze import analyze
from pyrror.DiscrepancyMonitoring.collect import collect_from_query
from pyrror.Error import Error


def get_alignment_config(discrepancy_monitoring):
    r = requests.get("%s/%s/%s/config" % (discrepancy_monitoring.monitoring_discrepancy_url,
                                          discrepancy_monitoring.client_id,
                                          discrepancy_monitoring.cod)).json()
    if r.get("error"):
        discrepancy_monitoring.error.log_error(function_name="get_alignment_config", error=r.get("error"))
    return r.get("config")


class DiscrepancyMonitoring:
    def __init__(self, dbstream, client_id, discrepancy_code, monitoring_url):
        self.client_id = client_id
        self.dbstream = dbstream
        self.code = discrepancy_code
        self.monitoring_url = monitoring_url
        self.monitoring_discrepancy_url = monitoring_url + "/api/monitoring/discrepancy/"
        self.error = Error(
            monitoring_error_url=monitoring_url + "/api/monitoring/error_to_slack/",
            client_id=client_id
        )

    def collect_from_query(self, query_result, source):
        collect_from_query(self, query_result, source)

    def analyze(self):
        analyze(self)
