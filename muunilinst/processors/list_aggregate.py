from typing import Any, List, Dict


def pre_aggregated(
        payload: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Aggregate a list of pre-aggregated data dictionaries.

    Parameters
    ----------
    payload : List[Dict[str, Any]]
        Data Payload.

    Examples
    --------
    >>> pre_aggregated([{
    >>>     "key": {"key_1": "some", "key_2": "thing"},
    >>>     "data": {"date": "2023-01-01", "value": [10.0, 20.0, 30.0], "value_2": [10.0, 20.0, 30.0]}
    >>> },
    >>> {
    >>>     "key": {"key_1": "some", "key_3": "thing"},
    >>>     "data": {"date": "2023-01-01", "value": [10.0, 20.0]}
    >>> }
    >>> ])

    """
    groups = []
    for item in payload:
        groups.append({
            "key": item.get("key"),
            "data": {
                "data_payload": sum(item.get("data").get(data_payload))
                for data_payload in item.get("data")
            }
        })

    return groups
