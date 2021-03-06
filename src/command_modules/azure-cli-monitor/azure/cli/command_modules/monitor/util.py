# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from datetime import datetime, timedelta

# ISO format with explicit indication of timezone
DATE_TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


def get_resource_group_location(cli_ctx, name):
    from azure.cli.core.commands.client_factory import get_mgmt_service_client
    from azure.cli.core.profiles import ResourceType

    # pylint: disable=no-member
    return get_mgmt_service_client(cli_ctx, ResourceType.MGMT_RESOURCE_RESOURCES).resource_groups.get(name).location


def get_operator_map():
    from azure.mgmt.monitor.models import ConditionOperator
    return {'>': ConditionOperator.greater_than.value, '>=': ConditionOperator.greater_than_or_equal.value,
            '<': ConditionOperator.less_than, '<=': ConditionOperator.less_than_or_equal}


def get_aggregation_map():
    from azure.mgmt.monitor.models import TimeAggregationOperator
    return {'avg': TimeAggregationOperator.average.value, 'min': TimeAggregationOperator.minimum.value,
            'max': TimeAggregationOperator.maximum.value, 'total': TimeAggregationOperator.total.value,
            'last': TimeAggregationOperator.last.value}


def validate_time_range_and_add_defaults(start_time, end_time, formatter='startTime eq {} and endTime eq {}'):
    try:
        end_time = datetime.strptime(end_time, DATE_TIME_FORMAT) if end_time else datetime.utcnow()
    except ValueError:
        raise ValueError("Input '{}' is not valid datetime. Valid example: 2000-12-31T12:59:59Z".format(end_time))

    try:
        start_time = datetime.strptime(start_time, DATE_TIME_FORMAT) if start_time else end_time - timedelta(hours=1)
        if start_time >= end_time:
            raise ValueError("Start time cannot be later than end time.")
    except ValueError:
        raise ValueError("Input '{}' is not valid datetime. Valid example: 2000-12-31T12:59:59Z".format(start_time))

    return formatter.format(start_time.strftime('%Y-%m-%dT%H:%M:%SZ'), end_time.strftime('%Y-%m-%dT%H:%M:%SZ'))
