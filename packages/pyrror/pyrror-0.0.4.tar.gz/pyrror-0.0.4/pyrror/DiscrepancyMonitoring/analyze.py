import json
import os
import requests
from pyrror.DiscrepancyMonitoring.DiscrepancyMonitoring import get_alignment_config


def get_test(discrepancy_monitoring, _alignment):
    dimensions_string = ",".join(_alignment["dimensions"])
    comparison_metrics = [
        "lag(%(metric)s) over (partition by %(dimensions_string)s order by source) as comparison_%(metric)s"
        % {"metric": metric, 'dimensions_string': dimensions_string}
        for metric in _alignment["metrics"]
    ]
    comparison_metrics_string = ",".join(comparison_metrics)

    check_metrics = [
        "(%(metric)s - comparison_%(metric)s)::float/comparison_%(metric)s as check_%(metric)s"
        % {"metric": metric}
        for metric in _alignment["metrics"]
    ]
    check_metrics_string = ",".join(check_metrics)

    query = """
    with inter as (SELECT
    *,
           rank() over (partition by source order by created_at desc) as rom_numb
    FROM __monitoring.%(alignment)s),
         inter2 as (
             select *,
                    lag(source) over (partition by %(dimensions_string)s order by source) as comparison_source,
                    %(comparison_metrics_string)s

             from inter
             where rom_numb = 1
         )
    select 
    %(check_metrics_string)s 
    , * from inter2
    where comparison_source is not null;
    """ % {
        "alignment": discrepancy_monitoring.code,
        "dimensions_string": dimensions_string,
        "comparison_metrics_string": comparison_metrics_string,
        "check_metrics_string": check_metrics_string
    }
    return discrepancy_monitoring.dbstream.execute_query(query)


def analyze(discrepancy_monitoring):
    _alignment = get_alignment_config(discrepancy_monitoring)
    _test = get_test(discrepancy_monitoring, _alignment)
    for element in _test:
        for metric in _alignment["metrics"]:
            if element["check_" + metric] > 0:
                dimensions = {}
                for d in _alignment["dimensions"]:
                    dimensions.update({d: element[d]})
                _error_dict = {
                    "client_id": discrepancy_monitoring.client,
                    "code": discrepancy_monitoring.code,
                    "source": element["source"],
                    "comparison_source": element["comparison_source"],
                    "metric": metric,
                    "error": element["check_" + metric],
                    "dimensions": dimensions,
                }
                requests.post(url=os.environ["MONITORING_DISCREPANCY_URL"], data=json.dumps(_error_dict, default=str))
