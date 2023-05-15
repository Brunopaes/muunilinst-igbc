"""Module for aggregating nested dictionaries. It can handle multiple
aggregation functions (sum, min, max and arithmetic average)."""

from collections import defaultdict
from typing import Any, DefaultDict, Dict, List, Optional, Tuple


def aggregate(
    payload: List[Dict[str, Any]],
    keys: List[Dict[str, Any]],
    values: List[str],
    aggregation_function: Optional[str] = "sum",
) -> List[Dict[str, Any]]:
    """Aggregate entrypoint. It filters the payload by the given keys,
    values and applies a given aggregation function.

    Parameters
    ----------
    payload: List[Dict[str, Any]]
        Dictionary containing payload data.

    keys: List[Dict[str, Any]]
        List of Dict paths in "key" or "data" objects.

    values: List[str]
        List of to be aggregated values.

    aggregation_function : Optional[str]
        Aggregation function; default function is "sum" (if not passed
        or passed with typo).

    Returns
    -------
    aggregated_list : List[Dict[str, Any]]
        List of aggregated Dicts.

    Examples
    --------
    >>> aggregate(
    >>>     payload=[
    >>>         {
    >>>             "key": {"key_1": "aaa"},
    >>>             "data": {"date": "2023-01-01", "value": 10}
    >>>         },
    >>>         {
    >>>             "key": {"key_1": "aaa"},
    >>>             "data": {"date": "2023-01-01", "value": 10}
    >>>         },
    >>>         {
    >>>             "key": {"key_1": "bbb"},
    >>>             "data": {"date": "2023-01-01", "value": 10}
    >>>         },
    >>>         {
    >>>             "key": {"key_1": "bbb"},
    >>>             "data": {"date": "2023-01-02", "value": 10}
    >>>         },
    >>>     ],
    >>>     keys=[{"key": "key_1"}, {"data": "date"}],
    >>>     values=["value", "value_2"],
    >>>     aggregation_function="sum"
    >>> )
    [
        {
            "key": {"key_1": "aaa"},
            "data": {"date": "2023-01-01", "value": 20}
        },
        {
            "key": {"key_1": "bbb"},
            "data": {"date": "2023-01-01", "value": 10}
        },
        {
            "key": {"key_1": "bbb"},
            "data": {"date": "2023-01-02", "value": 10}
        },
    ]

    """
    return reducing_dimensionality(
        aggregated_map=filtering_keys(payload, keys, values),
        aggregation_function=aggregation_function,
    )


def filtering_keys(
    payload: List[Dict[str, Any]],
    keys: List[Dict[str, Any]],
    values: List[str],
) -> DefaultDict[Tuple[Tuple[str, str], Tuple[str, str]], Dict]:
    """Filters the payload dict by the given keys and values.

    Parameters
    ----------
    payload: List[Dict[str, Any]]
        Dictionary containing payload data.

    keys: List[Dict[str, Any]]
        List of Dict paths in "key" or "data" objects.

    values: List[str]
        List of to be aggregated values.

    Returns
    -------
    aggregated_map : DefaultDict[List, Dict]
        Mapping of keys to aggregate data objects.

    Examples
    --------
    >>> filtering_keys(
    >>>     payload=[{
    >>>         "key": {"tech": "hydro", "region": "aaa"},
    >>>         "data": {"reference_date": "2023-01-01", "report_value": 10}
    >>>     }],
    >>>     keys=[
    >>>         {"key": "tech"},
    >>>         {"key": "region"},
    >>>         {"data": "reference_date"}
    >>>     ],
    >>>     values=["report_value"]
    >>> )
    defaultdict(dict, {
        (('tech', 'hydro'), ('region', 'aaa')): defaultdict(dict, {
            (('reference_date', '2023-01-01'),): defaultdict(list, {
                'report_value': [10]
            })
        })
    })

    """
    aggregated_map = \
        defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for item in payload:
        key_values = tuple(
            (k, item["key"].get(k)) for key in keys
            for k in key.values() if k in item["key"]
        )
        data_values = tuple(
            (k, item["data"].get(k)) for key in keys
            for k in key.values() if k in item["data"]
        )

        for value in values:
            aggregated_map[key_values][data_values][value].append(
                item["data"].get(value, 0)
            )

    return aggregated_map


def reducing_dimensionality(
    aggregated_map: DefaultDict[Tuple[Tuple[str, str], Tuple[str, str]], Dict],
    aggregation_function: Optional[str] = "sum",
) -> List[Dict[str, Any]]:
    """Reduces dimensionality by aggregating data objects.

    Parameters
    ----------
    aggregated_map : DefaultDict[Tuple[Tuple[str, str], Tuple[str, str]], Dict]
        Mapping of keys to aggregate data objects.

    aggregation_function : Optional[str]
        Aggregation function; default function is "sum" (if not passed
        or passed with typo).

    Returns
    -------
    aggregated_list : List[Dict[str, Any]]
        List of aggregated Dicts.

    Examples
    --------
    >>> reducing_dimensionality(
    >>>     aggregated_map=defaultdict(dict, {
    >>>         (('tech', 'hydro'), ('region', 'aaa')): defaultdict(dict, {
    >>>             (('reference_date', '2023-01-01'),): defaultdict(list, {
    >>>                 'report_value': [10, 20, 30]
    >>>             })
    >>>         })
    >>>     }),
    >>>     aggregation_function="min"
    >>> )
    [{
        'key': {'tech': 'hydro', 'region': 'aaa'},
        'data': {'reference_date': '2023-01-01', 'report_value': 10}
    }]

    """
    aggregated_list = []
    for key_values, data_values_map in aggregated_map.items():
        for data_values, values_map in data_values_map.items():
            aggregated_list.append({
                "key": dict(key_values),
                "data": dict(
                    data_values,
                    **aggregation_functions(
                        values_map, aggregation_function
                    )
                )}
            )

    return aggregated_list


def aggregation_functions(
        value_map: DefaultDict[str, List],
        aggregation_function: Optional[str] = "sum"
) -> DefaultDict[Any, int]:
    """Selects and Applies the given aggregation function (the default).

    Parameters
    ----------
    value_map : DefaultDict[str, List]
        List of to be aggregated values.

    aggregation_function : Optional[str]
        Aggregation function; default function is "sum" (if not passed
        or passed with typo).

    Returns
    -------
    aggregated_dict : DefaultDict[Any, int]
        Dictionary with aggregated values.

    Examples
    --------
    >>> aggregation_functions(
    >>>     value_map=defaultdict(list, {"reported_value": [10, 20, 30]}),
    >>>     aggregation_function="min"
    >>> )
    defaultdict(int, {"reported_value": 10})

    """
    aggregated_dict = defaultdict(int)
    for key, value_list in value_map.items():
        aggregated_dict[key] = {
            "sum": sum,
            "min": min,
            "max": max,
            "avg": arithmetic_average,
        }.get(aggregation_function, sum)(value_list)

    return aggregated_dict


def arithmetic_average(values_list: List[Any]) -> float:
    """Applies arithmetic average in a list.

    Parameters
    ----------
    values_list : List[Any]
        List of values to be aggregated.

    Returns
    -------
    arithmetic_average : float
        Calculated arithmetic average.

    Examples
    --------
    >>> arithmetic_average([10, 10, 5, 5])
    7.5

    >>> arithmetic_average([10, 8])
    9.0

    """
    return sum(values_list) / len(values_list)
