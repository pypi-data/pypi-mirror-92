import datetime
import pandas
from pyrror.DiscrepancyMonitoring.DiscrepancyMonitoring import get_alignment_config


def send(discrepancy_monitoring, query_result, source):
    table_name = discrepancy_monitoring.code
    schema_name = "__monitoring"

    if not query_result:
        return 0

    __dict_added__ = {
        "source": source,
        "created_at": datetime.datetime.now()
    }

    dict_columns = query_result[0]
    dict_columns.update(__dict_added__)
    columns_name = list(dict_columns.keys())

    rows = []
    for r in query_result:
        r.update(__dict_added__)
        row = []
        for c in columns_name:
            row.append(r[c])
        rows.append(row)

    monitoring_data = {
        "table_name": "%s.%s" % (schema_name, table_name),
        "columns_name": columns_name,
        "rows": rows
    }
    discrepancy_monitoring.dbstream.send_data(monitoring_data, replace=False)


def collect_from_query(discrepancy_monitoring, query_result, source):
    _alignment = get_alignment_config(discrepancy_monitoring)
    _mapping = _alignment.get("sources").get(source).get("mapping")
    df = pandas.DataFrame(query_result)
    df = df.rename(columns=_mapping)
    _filter = _alignment.get("filter")
    if _filter:
        df = df[eval(_filter.strip())]
    _list_to_group = []
    for d in _alignment["dimensions"]:
        if d in df.columns:
            _list_to_group.append(d)
    if _list_to_group:
        df = df.groupby(_list_to_group, as_index=False).sum()

        _data = df.to_dict(orient="records")
    else:
        _data = df.sum()

    send(discrepancy_monitoring=discrepancy_monitoring, query_result=_data, source=source)
