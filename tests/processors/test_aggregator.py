from collections import defaultdict

from muunilinst.processors import aggregator


def test_aggregate():
    payload = [
        {
            "key": {"tech": "hydro", "region": "aaa"},
            "data": {"reference_date": "2023-01-01", "report_value": 9},
        },
        {
            "key": {"tech": "hydro", "region": "aaa"},
            "data": {"reference_date": "2023-01-01", "report_value": 1},
        },
        {
            "key": {"tech": "hydro", "region": "bbb"},
            "data": {"reference_date": "2023-01-01", "report_value": 5},
        },
        {
            "key": {"tech": "hydro", "region": "bbb"},
            "data": {"reference_date": "2023-01-01", "report_value": 5},
        },
    ]
    keys = [{"key": "tech"}, {"key": "region"}, {"data": "reference_date"}]
    values = ["report_value"]

    # Test Case #01: min() aggregation function
    expected = [
        {
            "key": {"tech": "hydro", "region": "aaa"},
            "data": {"reference_date": "2023-01-01", "report_value": 1},
        },
        {
            "key": {"tech": "hydro", "region": "bbb"},
            "data": {"reference_date": "2023-01-01", "report_value": 5},
        },
    ]
    result = aggregator.aggregate(
        payload=payload,
        keys=keys,
        values=values,
        aggregation_function="min"
    )

    assert expected == result

    # Test Case #02: max() aggregation function
    expected = [
        {
            "key": {"tech": "hydro", "region": "aaa"},
            "data": {"reference_date": "2023-01-01", "report_value": 9},
        },
        {
            "key": {"tech": "hydro", "region": "bbb"},
            "data": {"reference_date": "2023-01-01", "report_value": 5},
        },
    ]
    result = aggregator.aggregate(
        payload=payload,
        keys=keys,
        values=values,
        aggregation_function="max"
    )

    assert expected == result

    # Test Case #03: sum() aggregation function
    expected = [
        {
            "key": {"tech": "hydro", "region": "aaa"},
            "data": {"reference_date": "2023-01-01", "report_value": 10},
        },
        {
            "key": {"tech": "hydro", "region": "bbb"},
            "data": {"reference_date": "2023-01-01", "report_value": 10},
        },
    ]
    result = aggregator.aggregate(
        payload=payload,
        keys=keys,
        values=values,
        aggregation_function="sum"
    )

    assert expected == result

    # Test Case #04: avg() aggregation function
    expected = [
        {
            "key": {"tech": "hydro", "region": "aaa"},
            "data": {"reference_date": "2023-01-01", "report_value": 5},
        },
        {
            "key": {"tech": "hydro", "region": "bbb"},
            "data": {"reference_date": "2023-01-01", "report_value": 5},
        },
    ]
    result = aggregator.aggregate(
        payload=payload,
        keys=keys,
        values=values,
        aggregation_function="avg"
    )

    assert expected == result


def test_filtering_keys():
    expected = defaultdict(
        dict,
        {
            (("tech", "hydro"), ("region", "aaa")): defaultdict(
                dict,
                {
                    (("reference_date", "2023-01-01"),): defaultdict(
                        list, {"report_value": [10]}
                    )
                },
            )
        },
    )
    result = aggregator.filtering_keys(
        payload=[
            {
                "key": {"tech": "hydro", "region": "aaa"},
                "data": {"reference_date": "2023-01-01", "report_value": 10},
            }
        ],
        keys=[{"key": "tech"}, {"key": "region"}, {"data": "reference_date"}],
        values=["report_value"],
    )

    assert expected == result


def test_reducing_dimensionality():
    # Test Case #01: min() aggregation function
    expected = [
        {
            "key": {"tech": "hydro", "region": "aaa"},
            "data": {"reference_date": "2023-01-01", "report_value": 10},
        }
    ]
    result = aggregator.reducing_dimensionality(
        aggregated_map=defaultdict(
            dict,
            {
                (("tech", "hydro"), ("region", "aaa")): defaultdict(
                    dict,
                    {
                        (("reference_date", "2023-01-01"),): defaultdict(
                            list, {"report_value": [10, 20, 30]}
                        )
                    },
                )
            },
        ),
        aggregation_function="min",
    )

    assert result == expected

    # Test Case #02: max() aggregation function
    expected = [
        {
            "key": {"tech": "hydro", "region": "aaa"},
            "data": {"reference_date": "2023-01-01", "report_value": 30},
        }
    ]
    result = aggregator.reducing_dimensionality(
        aggregated_map=defaultdict(
            dict,
            {
                (("tech", "hydro"), ("region", "aaa")): defaultdict(
                    dict,
                    {
                        (("reference_date", "2023-01-01"),): defaultdict(
                            list, {"report_value": [10, 20, 30]}
                        )
                    },
                )
            },
        ),
        aggregation_function="max",
    )

    assert result == expected

    # Test Case #03: sum() aggregation function
    expected = [
        {
            "key": {"tech": "hydro", "region": "aaa"},
            "data": {"reference_date": "2023-01-01", "report_value": 60},
        }
    ]
    result = aggregator.reducing_dimensionality(
        aggregated_map=defaultdict(
            dict,
            {
                (("tech", "hydro"), ("region", "aaa")): defaultdict(
                    dict,
                    {
                        (("reference_date", "2023-01-01"),): defaultdict(
                            list, {"report_value": [10, 20, 30]}
                        )
                    },
                )
            },
        ),
        aggregation_function="sum",
    )

    assert result == expected

    # Test Case #04: avg() aggregation function
    expected = [
        {
            "key": {"tech": "hydro", "region": "aaa"},
            "data": {"reference_date": "2023-01-01", "report_value": 20},
        }
    ]
    result = aggregator.reducing_dimensionality(
        aggregated_map=defaultdict(
            dict,
            {
                (("tech", "hydro"), ("region", "aaa")): defaultdict(
                    dict,
                    {
                        (("reference_date", "2023-01-01"),): defaultdict(
                            list, {"report_value": [10, 20, 30]}
                        )
                    },
                )
            },
        ),
        aggregation_function="avg",
    )

    assert result == expected


def test_aggregation_functions():
    # Test Case #01: min() aggregation function
    expected_result = defaultdict(int, {"reported_value": 10})
    result = aggregator.aggregation_functions(
        value_map=defaultdict(list, {"reported_value": [10, 20, 30]}),
        aggregation_function="min",
    )

    assert result == expected_result

    # Test Case #02: max() aggregation function
    expected_result = defaultdict(int, {"reported_value": 30})
    result = aggregator.aggregation_functions(
        value_map=defaultdict(list, {"reported_value": [10, 20, 30]}),
        aggregation_function="max",
    )

    assert result == expected_result

    # Test Case #03: sum() aggregation function
    expected_result = defaultdict(int, {"reported_value": 60})
    result = aggregator.aggregation_functions(
        value_map=defaultdict(list, {"reported_value": [10, 20, 30]}),
        aggregation_function="sum",
    )

    assert result == expected_result

    # Test Case #04: arithmetic_average() aggregation function
    expected_result = defaultdict(int, {"reported_value": 20})
    result = aggregator.aggregation_functions(
        value_map=defaultdict(list, {"reported_value": [10, 20, 30]}),
        aggregation_function="avg",
    )

    assert result == expected_result


def test_arithmetic_average():
    # Test Case #01: expected result 0.0
    expected_result = 0.0
    result = aggregator.arithmetic_average([0, 0, 0, 0])

    assert result == expected_result

    # Test Case #02: expected result 7.5
    expected_result = 7.5
    result = aggregator.arithmetic_average([10, 10, 5, 5])

    assert result == expected_result
