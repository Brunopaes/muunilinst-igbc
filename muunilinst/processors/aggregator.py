from collections import defaultdict
from typing import Any, Dict, List


def aggregate(
        payload: List[Dict[str, Any]],
        keys: List[Dict[str, Any]],
        values: List[str],
        aggregation_type: str = "sum"
) -> List[Dict[str, Any]]:
    aggregated_map = defaultdict(
        lambda: defaultdict(lambda: defaultdict(list))
    )

    for item in payload:
        key_values = tuple((k, item["key"].get(k)) for key in keys
                           for k in key.values() if k in item["key"])
        data_values = tuple((k, item["data"].get(k)) for key in keys
                            for k in key.values() if k in item["data"])

        for value in values:
            aggregated_map[key_values][data_values][value].append(
                item["data"].get(value, 0)
            )

    aggregated_list = []
    for key_values, data_values_map in aggregated_map.items():
        for data_values, value_map in data_values_map.items():
            aggregated_list.append({
                "key": dict(key_values),
                "data": dict(data_values, **sum_dict_lists(
                    value_map, aggregation_type
                ))
            })

    return aggregated_list


def sum_dict_lists(input_dict, aggregation_type):
    aggregation_functions = {
        "sum": sum,
        "min": min,
        "max": max,
        "avg": average
    }
    aggregated_dict = defaultdict(int)
    for key, value_list in input_dict.items():
        aggregated_dict[key] = aggregation_functions.get(
            aggregation_type, sum
        )(value_list)

    return aggregated_dict


def average(values_list):
    return sum(values_list) / len(values_list)
