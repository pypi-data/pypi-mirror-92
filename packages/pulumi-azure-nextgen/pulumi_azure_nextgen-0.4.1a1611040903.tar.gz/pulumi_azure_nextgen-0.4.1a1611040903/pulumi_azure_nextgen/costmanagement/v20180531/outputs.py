# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs
from ._enums import *

__all__ = [
    'ReportConfigAggregationResponse',
    'ReportConfigComparisonExpressionResponse',
    'ReportConfigDatasetConfigurationResponse',
    'ReportConfigDatasetResponse',
    'ReportConfigDefinitionResponse',
    'ReportConfigDeliveryDestinationResponse',
    'ReportConfigDeliveryInfoResponse',
    'ReportConfigFilterResponse',
    'ReportConfigGroupingResponse',
    'ReportConfigRecurrencePeriodResponse',
    'ReportConfigScheduleResponse',
    'ReportConfigTimePeriodResponse',
]

@pulumi.output_type
class ReportConfigAggregationResponse(dict):
    """
    The aggregation expression to be used in the report.
    """
    def __init__(__self__, *,
                 function: str,
                 name: str):
        """
        The aggregation expression to be used in the report.
        :param str function: The name of the aggregation function to use.
        :param str name: The name of the column to aggregate.
        """
        pulumi.set(__self__, "function", function)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def function(self) -> str:
        """
        The name of the aggregation function to use.
        """
        return pulumi.get(self, "function")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the column to aggregate.
        """
        return pulumi.get(self, "name")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ReportConfigComparisonExpressionResponse(dict):
    """
    The comparison expression to be used in the report.
    """
    def __init__(__self__, *,
                 name: str,
                 operator: str,
                 values: Sequence[str]):
        """
        The comparison expression to be used in the report.
        :param str name: The name of the column to use in comparison.
        :param str operator: The operator to use for comparison.
        :param Sequence[str] values: Array of values to use for comparison
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "operator", operator)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the column to use in comparison.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def operator(self) -> str:
        """
        The operator to use for comparison.
        """
        return pulumi.get(self, "operator")

    @property
    @pulumi.getter
    def values(self) -> Sequence[str]:
        """
        Array of values to use for comparison
        """
        return pulumi.get(self, "values")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ReportConfigDatasetConfigurationResponse(dict):
    """
    The configuration of dataset in the report.
    """
    def __init__(__self__, *,
                 columns: Optional[Sequence[str]] = None):
        """
        The configuration of dataset in the report.
        :param Sequence[str] columns: Array of column names to be included in the report. Any valid report column name is allowed. If not provided, then report includes all columns.
        """
        if columns is not None:
            pulumi.set(__self__, "columns", columns)

    @property
    @pulumi.getter
    def columns(self) -> Optional[Sequence[str]]:
        """
        Array of column names to be included in the report. Any valid report column name is allowed. If not provided, then report includes all columns.
        """
        return pulumi.get(self, "columns")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ReportConfigDatasetResponse(dict):
    """
    The definition of data present in the report.
    """
    def __init__(__self__, *,
                 aggregation: Optional[Mapping[str, 'outputs.ReportConfigAggregationResponse']] = None,
                 configuration: Optional['outputs.ReportConfigDatasetConfigurationResponse'] = None,
                 filter: Optional['outputs.ReportConfigFilterResponse'] = None,
                 granularity: Optional[str] = None,
                 grouping: Optional[Sequence['outputs.ReportConfigGroupingResponse']] = None):
        """
        The definition of data present in the report.
        :param Mapping[str, 'ReportConfigAggregationResponseArgs'] aggregation: Dictionary of aggregation expression to use in the report. The key of each item in the dictionary is the alias for the aggregated column. Report can have up to 2 aggregation clauses.
        :param 'ReportConfigDatasetConfigurationResponseArgs' configuration: Has configuration information for the data in the report. The configuration will be ignored if aggregation and grouping are provided.
        :param 'ReportConfigFilterResponseArgs' filter: Has filter expression to use in the report.
        :param str granularity: The granularity of rows in the report.
        :param Sequence['ReportConfigGroupingResponseArgs'] grouping: Array of group by expression to use in the report. Report can have up to 2 group by clauses.
        """
        if aggregation is not None:
            pulumi.set(__self__, "aggregation", aggregation)
        if configuration is not None:
            pulumi.set(__self__, "configuration", configuration)
        if filter is not None:
            pulumi.set(__self__, "filter", filter)
        if granularity is not None:
            pulumi.set(__self__, "granularity", granularity)
        if grouping is not None:
            pulumi.set(__self__, "grouping", grouping)

    @property
    @pulumi.getter
    def aggregation(self) -> Optional[Mapping[str, 'outputs.ReportConfigAggregationResponse']]:
        """
        Dictionary of aggregation expression to use in the report. The key of each item in the dictionary is the alias for the aggregated column. Report can have up to 2 aggregation clauses.
        """
        return pulumi.get(self, "aggregation")

    @property
    @pulumi.getter
    def configuration(self) -> Optional['outputs.ReportConfigDatasetConfigurationResponse']:
        """
        Has configuration information for the data in the report. The configuration will be ignored if aggregation and grouping are provided.
        """
        return pulumi.get(self, "configuration")

    @property
    @pulumi.getter
    def filter(self) -> Optional['outputs.ReportConfigFilterResponse']:
        """
        Has filter expression to use in the report.
        """
        return pulumi.get(self, "filter")

    @property
    @pulumi.getter
    def granularity(self) -> Optional[str]:
        """
        The granularity of rows in the report.
        """
        return pulumi.get(self, "granularity")

    @property
    @pulumi.getter
    def grouping(self) -> Optional[Sequence['outputs.ReportConfigGroupingResponse']]:
        """
        Array of group by expression to use in the report. Report can have up to 2 group by clauses.
        """
        return pulumi.get(self, "grouping")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ReportConfigDefinitionResponse(dict):
    """
    The definition of a report config.
    """
    def __init__(__self__, *,
                 timeframe: str,
                 type: str,
                 dataset: Optional['outputs.ReportConfigDatasetResponse'] = None,
                 time_period: Optional['outputs.ReportConfigTimePeriodResponse'] = None):
        """
        The definition of a report config.
        :param str timeframe: The time frame for pulling data for the report. If custom, then a specific time period must be provided.
        :param str type: The type of the report.
        :param 'ReportConfigDatasetResponseArgs' dataset: Has definition for data in this report config.
        :param 'ReportConfigTimePeriodResponseArgs' time_period: Has time period for pulling data for the report.
        """
        pulumi.set(__self__, "timeframe", timeframe)
        pulumi.set(__self__, "type", type)
        if dataset is not None:
            pulumi.set(__self__, "dataset", dataset)
        if time_period is not None:
            pulumi.set(__self__, "time_period", time_period)

    @property
    @pulumi.getter
    def timeframe(self) -> str:
        """
        The time frame for pulling data for the report. If custom, then a specific time period must be provided.
        """
        return pulumi.get(self, "timeframe")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the report.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def dataset(self) -> Optional['outputs.ReportConfigDatasetResponse']:
        """
        Has definition for data in this report config.
        """
        return pulumi.get(self, "dataset")

    @property
    @pulumi.getter(name="timePeriod")
    def time_period(self) -> Optional['outputs.ReportConfigTimePeriodResponse']:
        """
        Has time period for pulling data for the report.
        """
        return pulumi.get(self, "time_period")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ReportConfigDeliveryDestinationResponse(dict):
    """
    The destination information for the delivery of the report.
    """
    def __init__(__self__, *,
                 container: str,
                 resource_id: str,
                 root_folder_path: Optional[str] = None):
        """
        The destination information for the delivery of the report.
        :param str container: The name of the container where reports will be uploaded.
        :param str resource_id: The resource id of the storage account where reports will be delivered.
        :param str root_folder_path: The name of the directory where reports will be uploaded.
        """
        pulumi.set(__self__, "container", container)
        pulumi.set(__self__, "resource_id", resource_id)
        if root_folder_path is not None:
            pulumi.set(__self__, "root_folder_path", root_folder_path)

    @property
    @pulumi.getter
    def container(self) -> str:
        """
        The name of the container where reports will be uploaded.
        """
        return pulumi.get(self, "container")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> str:
        """
        The resource id of the storage account where reports will be delivered.
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter(name="rootFolderPath")
    def root_folder_path(self) -> Optional[str]:
        """
        The name of the directory where reports will be uploaded.
        """
        return pulumi.get(self, "root_folder_path")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ReportConfigDeliveryInfoResponse(dict):
    """
    The delivery information associated with a report config.
    """
    def __init__(__self__, *,
                 destination: 'outputs.ReportConfigDeliveryDestinationResponse'):
        """
        The delivery information associated with a report config.
        :param 'ReportConfigDeliveryDestinationResponseArgs' destination: Has destination for the report being delivered.
        """
        pulumi.set(__self__, "destination", destination)

    @property
    @pulumi.getter
    def destination(self) -> 'outputs.ReportConfigDeliveryDestinationResponse':
        """
        Has destination for the report being delivered.
        """
        return pulumi.get(self, "destination")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ReportConfigFilterResponse(dict):
    """
    The filter expression to be used in the report.
    """
    def __init__(__self__, *,
                 and_: Optional[Sequence['outputs.ReportConfigFilterResponse']] = None,
                 dimension: Optional['outputs.ReportConfigComparisonExpressionResponse'] = None,
                 not_: Optional['outputs.ReportConfigFilterResponse'] = None,
                 or_: Optional[Sequence['outputs.ReportConfigFilterResponse']] = None,
                 tag: Optional['outputs.ReportConfigComparisonExpressionResponse'] = None):
        """
        The filter expression to be used in the report.
        :param Sequence['ReportConfigFilterResponseArgs'] and_: The logical "AND" expression. Must have at least 2 items.
        :param 'ReportConfigComparisonExpressionResponseArgs' dimension: Has comparison expression for a dimension
        :param 'ReportConfigFilterResponseArgs' not_: The logical "NOT" expression.
        :param Sequence['ReportConfigFilterResponseArgs'] or_: The logical "OR" expression. Must have at least 2 items.
        :param 'ReportConfigComparisonExpressionResponseArgs' tag: Has comparison expression for a tag
        """
        if and_ is not None:
            pulumi.set(__self__, "and_", and_)
        if dimension is not None:
            pulumi.set(__self__, "dimension", dimension)
        if not_ is not None:
            pulumi.set(__self__, "not_", not_)
        if or_ is not None:
            pulumi.set(__self__, "or_", or_)
        if tag is not None:
            pulumi.set(__self__, "tag", tag)

    @property
    @pulumi.getter(name="and")
    def and_(self) -> Optional[Sequence['outputs.ReportConfigFilterResponse']]:
        """
        The logical "AND" expression. Must have at least 2 items.
        """
        return pulumi.get(self, "and_")

    @property
    @pulumi.getter
    def dimension(self) -> Optional['outputs.ReportConfigComparisonExpressionResponse']:
        """
        Has comparison expression for a dimension
        """
        return pulumi.get(self, "dimension")

    @property
    @pulumi.getter(name="not")
    def not_(self) -> Optional['outputs.ReportConfigFilterResponse']:
        """
        The logical "NOT" expression.
        """
        return pulumi.get(self, "not_")

    @property
    @pulumi.getter(name="or")
    def or_(self) -> Optional[Sequence['outputs.ReportConfigFilterResponse']]:
        """
        The logical "OR" expression. Must have at least 2 items.
        """
        return pulumi.get(self, "or_")

    @property
    @pulumi.getter
    def tag(self) -> Optional['outputs.ReportConfigComparisonExpressionResponse']:
        """
        Has comparison expression for a tag
        """
        return pulumi.get(self, "tag")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ReportConfigGroupingResponse(dict):
    """
    The group by expression to be used in the report.
    """
    def __init__(__self__, *,
                 column_type: str,
                 name: str):
        """
        The group by expression to be used in the report.
        :param str column_type: Has type of the column to group.
        :param str name: The name of the column to group.
        """
        pulumi.set(__self__, "column_type", column_type)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="columnType")
    def column_type(self) -> str:
        """
        Has type of the column to group.
        """
        return pulumi.get(self, "column_type")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the column to group.
        """
        return pulumi.get(self, "name")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ReportConfigRecurrencePeriodResponse(dict):
    """
    The start and end date for recurrence schedule.
    """
    def __init__(__self__, *,
                 from_: str,
                 to: Optional[str] = None):
        """
        The start and end date for recurrence schedule.
        :param str from_: The start date of recurrence.
        :param str to: The end date of recurrence. If not provided, we default this to 10 years from the start date.
        """
        pulumi.set(__self__, "from_", from_)
        if to is not None:
            pulumi.set(__self__, "to", to)

    @property
    @pulumi.getter(name="from")
    def from_(self) -> str:
        """
        The start date of recurrence.
        """
        return pulumi.get(self, "from_")

    @property
    @pulumi.getter
    def to(self) -> Optional[str]:
        """
        The end date of recurrence. If not provided, we default this to 10 years from the start date.
        """
        return pulumi.get(self, "to")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ReportConfigScheduleResponse(dict):
    """
    The schedule associated with a report config.
    """
    def __init__(__self__, *,
                 recurrence: str,
                 recurrence_period: 'outputs.ReportConfigRecurrencePeriodResponse',
                 status: Optional[str] = None):
        """
        The schedule associated with a report config.
        :param str recurrence: The schedule recurrence.
        :param 'ReportConfigRecurrencePeriodResponseArgs' recurrence_period: Has start and end date of the recurrence. The start date must be in future. If present, the end date must be greater than start date.
        :param str status: The status of the schedule. Whether active or not. If inactive, the report's scheduled execution is paused.
        """
        pulumi.set(__self__, "recurrence", recurrence)
        pulumi.set(__self__, "recurrence_period", recurrence_period)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def recurrence(self) -> str:
        """
        The schedule recurrence.
        """
        return pulumi.get(self, "recurrence")

    @property
    @pulumi.getter(name="recurrencePeriod")
    def recurrence_period(self) -> 'outputs.ReportConfigRecurrencePeriodResponse':
        """
        Has start and end date of the recurrence. The start date must be in future. If present, the end date must be greater than start date.
        """
        return pulumi.get(self, "recurrence_period")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        The status of the schedule. Whether active or not. If inactive, the report's scheduled execution is paused.
        """
        return pulumi.get(self, "status")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ReportConfigTimePeriodResponse(dict):
    """
    The start and end date for pulling data for the report.
    """
    def __init__(__self__, *,
                 from_: str,
                 to: str):
        """
        The start and end date for pulling data for the report.
        :param str from_: The start date to pull data from.
        :param str to: The end date to pull data to.
        """
        pulumi.set(__self__, "from_", from_)
        pulumi.set(__self__, "to", to)

    @property
    @pulumi.getter(name="from")
    def from_(self) -> str:
        """
        The start date to pull data from.
        """
        return pulumi.get(self, "from_")

    @property
    @pulumi.getter
    def to(self) -> str:
        """
        The end date to pull data to.
        """
        return pulumi.get(self, "to")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


