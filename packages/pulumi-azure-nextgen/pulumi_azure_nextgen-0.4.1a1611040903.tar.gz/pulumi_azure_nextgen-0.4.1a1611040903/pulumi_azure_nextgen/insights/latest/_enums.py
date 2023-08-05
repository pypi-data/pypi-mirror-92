# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AggregationTypeEnum',
    'AlertSeverity',
    'ApplicationType',
    'ComparisonOperationType',
    'ConditionOperator',
    'ConditionalOperator',
    'CriterionType',
    'DynamicThresholdOperator',
    'DynamicThresholdSensitivity',
    'Enabled',
    'FavoriteType',
    'FlowType',
    'IngestionMode',
    'ItemScope',
    'ItemType',
    'Kind',
    'MetricStatisticType',
    'MetricTriggerType',
    'Odatatype',
    'OperationType',
    'Operator',
    'QueryType',
    'RecurrenceFrequency',
    'RequestSource',
    'ScaleDirection',
    'ScaleRuleMetricDimensionOperationType',
    'ScaleType',
    'TimeAggregationOperator',
    'TimeAggregationType',
    'WebTestKind',
]


class AggregationTypeEnum(str, Enum):
    """
    the criteria time aggregation types.
    """
    AVERAGE = "Average"
    COUNT = "Count"
    MINIMUM = "Minimum"
    MAXIMUM = "Maximum"
    TOTAL = "Total"


class AlertSeverity(str, Enum):
    """
    Severity of the alert
    """
    ZERO = "0"
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"


class ApplicationType(str, Enum):
    """
    Type of application being monitored.
    """
    WEB = "web"
    OTHER = "other"


class ComparisonOperationType(str, Enum):
    """
    the operator that is used to compare the metric data and the threshold.
    """
    EQUALS = "Equals"
    NOT_EQUALS = "NotEquals"
    GREATER_THAN = "GreaterThan"
    GREATER_THAN_OR_EQUAL = "GreaterThanOrEqual"
    LESS_THAN = "LessThan"
    LESS_THAN_OR_EQUAL = "LessThanOrEqual"


class ConditionOperator(str, Enum):
    """
    the operator used to compare the data and the threshold.
    """
    GREATER_THAN = "GreaterThan"
    GREATER_THAN_OR_EQUAL = "GreaterThanOrEqual"
    LESS_THAN = "LessThan"
    LESS_THAN_OR_EQUAL = "LessThanOrEqual"


class ConditionalOperator(str, Enum):
    """
    Evaluation operation for rule - 'GreaterThan' or 'LessThan.
    """
    GREATER_THAN = "GreaterThan"
    LESS_THAN = "LessThan"
    EQUAL = "Equal"


class CriterionType(str, Enum):
    """
    Specifies the type of threshold criteria
    """
    STATIC_THRESHOLD_CRITERION = "StaticThresholdCriterion"
    DYNAMIC_THRESHOLD_CRITERION = "DynamicThresholdCriterion"


class DynamicThresholdOperator(str, Enum):
    """
    The operator used to compare the metric value against the threshold.
    """
    GREATER_THAN = "GreaterThan"
    LESS_THAN = "LessThan"
    GREATER_OR_LESS_THAN = "GreaterOrLessThan"


class DynamicThresholdSensitivity(str, Enum):
    """
    The extent of deviation required to trigger an alert. This will affect how tight the threshold is to the metric series pattern.
    """
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class Enabled(str, Enum):
    """
    The flag which indicates whether the Log Search rule is enabled. Value should be true or false
    """
    TRUE = "true"
    FALSE = "false"


class FavoriteType(str, Enum):
    """
    Enum indicating if this favorite definition is owned by a specific user or is shared between all users with access to the Application Insights component.
    """
    SHARED = "shared"
    USER = "user"


class FlowType(str, Enum):
    """
    Used by the Application Insights system to determine what kind of flow this component was created by. This is to be set to 'Bluefield' when creating/updating a component via the REST API.
    """
    BLUEFIELD = "Bluefield"


class IngestionMode(str, Enum):
    """
    Indicates the flow of the ingestion.
    """
    APPLICATION_INSIGHTS = "ApplicationInsights"
    APPLICATION_INSIGHTS_WITH_DIAGNOSTIC_SETTINGS = "ApplicationInsightsWithDiagnosticSettings"
    LOG_ANALYTICS = "LogAnalytics"


class ItemScope(str, Enum):
    """
    Enum indicating if this item definition is owned by a specific user or is shared between all users with access to the Application Insights component.
    """
    SHARED = "shared"
    USER = "user"


class ItemType(str, Enum):
    """
    Enum indicating the type of the Analytics item.
    """
    QUERY = "query"
    FUNCTION = "function"
    FOLDER = "folder"
    RECENT = "recent"


class Kind(str, Enum):
    """
    The kind of workbook. Choices are user and shared.
    """
    USER = "user"
    SHARED = "shared"


class MetricStatisticType(str, Enum):
    """
    the metric statistic type. How the metrics from multiple instances are combined.
    """
    AVERAGE = "Average"
    MIN = "Min"
    MAX = "Max"
    SUM = "Sum"


class MetricTriggerType(str, Enum):
    """
    Metric Trigger Type - 'Consecutive' or 'Total'
    """
    CONSECUTIVE = "Consecutive"
    TOTAL = "Total"


class Odatatype(str, Enum):
    """
    specifies the type of the alert criteria.
    """
    MICROSOFT_AZURE_MONITOR_SINGLE_RESOURCE_MULTIPLE_METRIC_CRITERIA = "Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria"
    MICROSOFT_AZURE_MONITOR_MULTIPLE_RESOURCE_MULTIPLE_METRIC_CRITERIA = "Microsoft.Azure.Monitor.MultipleResourceMultipleMetricCriteria"
    MICROSOFT_AZURE_MONITOR_WEBTEST_LOCATION_AVAILABILITY_CRITERIA = "Microsoft.Azure.Monitor.WebtestLocationAvailabilityCriteria"


class OperationType(str, Enum):
    """
    the operation associated with the notification and its value must be "scale"
    """
    SCALE = "Scale"


class Operator(str, Enum):
    """
    Operator for dimension values
    """
    INCLUDE = "Include"


class QueryType(str, Enum):
    """
    Set value to 'ResultCount' .
    """
    RESULT_COUNT = "ResultCount"


class RecurrenceFrequency(str, Enum):
    """
    the recurrence frequency. How often the schedule profile should take effect. This value must be Week, meaning each week will have the same set of profiles. For example, to set a daily schedule, set **schedule** to every day of the week. The frequency property specifies that the schedule is repeated weekly.
    """
    NONE = "None"
    SECOND = "Second"
    MINUTE = "Minute"
    HOUR = "Hour"
    DAY = "Day"
    WEEK = "Week"
    MONTH = "Month"
    YEAR = "Year"


class RequestSource(str, Enum):
    """
    Describes what tool created this Application Insights component. Customers using this API should set this to the default 'rest'.
    """
    REST = "rest"


class ScaleDirection(str, Enum):
    """
    the scale direction. Whether the scaling action increases or decreases the number of instances.
    """
    NONE = "None"
    INCREASE = "Increase"
    DECREASE = "Decrease"


class ScaleRuleMetricDimensionOperationType(str, Enum):
    """
    the dimension operator. Only 'Equals' and 'NotEquals' are supported. 'Equals' being equal to any of the values. 'NotEquals' being not equal to all of the values
    """
    EQUALS = "Equals"
    NOT_EQUALS = "NotEquals"


class ScaleType(str, Enum):
    """
    the type of action that should occur when the scale rule fires.
    """
    CHANGE_COUNT = "ChangeCount"
    PERCENT_CHANGE_COUNT = "PercentChangeCount"
    EXACT_COUNT = "ExactCount"


class TimeAggregationOperator(str, Enum):
    """
    the time aggregation operator. How the data that are collected should be combined over time. The default value is the PrimaryAggregationType of the Metric.
    """
    AVERAGE = "Average"
    MINIMUM = "Minimum"
    MAXIMUM = "Maximum"
    TOTAL = "Total"
    LAST = "Last"


class TimeAggregationType(str, Enum):
    """
    time aggregation type. How the data that is collected should be combined over time. The default value is Average.
    """
    AVERAGE = "Average"
    MINIMUM = "Minimum"
    MAXIMUM = "Maximum"
    TOTAL = "Total"
    COUNT = "Count"
    LAST = "Last"


class WebTestKind(str, Enum):
    """
    The kind of web test this is, valid choices are ping and multistep.
    """
    PING = "ping"
    MULTISTEP = "multistep"
