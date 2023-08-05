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
    'LocationThresholdRuleConditionResponse',
    'ManagementEventAggregationConditionResponse',
    'ManagementEventRuleConditionResponse',
    'RetentionPolicyResponse',
    'RuleEmailActionResponse',
    'RuleManagementEventClaimsDataSourceResponse',
    'RuleManagementEventDataSourceResponse',
    'RuleMetricDataSourceResponse',
    'RuleWebhookActionResponse',
    'ThresholdRuleConditionResponse',
]

@pulumi.output_type
class LocationThresholdRuleConditionResponse(dict):
    """
    A rule condition based on a certain number of locations failing.
    """
    def __init__(__self__, *,
                 failed_location_count: int,
                 odata_type: str,
                 data_source: Optional[Any] = None,
                 window_size: Optional[str] = None):
        """
        A rule condition based on a certain number of locations failing.
        :param int failed_location_count: the number of locations that must fail to activate the alert.
        :param str odata_type: specifies the type of condition. This can be one of three types: ManagementEventRuleCondition (occurrences of management events), LocationThresholdRuleCondition (based on the number of failures of a web test), and ThresholdRuleCondition (based on the threshold of a metric).
               Expected value is 'Microsoft.Azure.Management.Insights.Models.LocationThresholdRuleCondition'.
        :param Union['RuleManagementEventDataSourceResponseArgs', 'RuleMetricDataSourceResponseArgs'] data_source: the resource from which the rule collects its data. For this type dataSource will always be of type RuleMetricDataSource.
        :param str window_size: the period of time (in ISO 8601 duration format) that is used to monitor alert activity based on the threshold. If specified then it must be between 5 minutes and 1 day.
        """
        pulumi.set(__self__, "failed_location_count", failed_location_count)
        pulumi.set(__self__, "odata_type", 'Microsoft.Azure.Management.Insights.Models.LocationThresholdRuleCondition')
        if data_source is not None:
            pulumi.set(__self__, "data_source", data_source)
        if window_size is not None:
            pulumi.set(__self__, "window_size", window_size)

    @property
    @pulumi.getter(name="failedLocationCount")
    def failed_location_count(self) -> int:
        """
        the number of locations that must fail to activate the alert.
        """
        return pulumi.get(self, "failed_location_count")

    @property
    @pulumi.getter(name="odataType")
    def odata_type(self) -> str:
        """
        specifies the type of condition. This can be one of three types: ManagementEventRuleCondition (occurrences of management events), LocationThresholdRuleCondition (based on the number of failures of a web test), and ThresholdRuleCondition (based on the threshold of a metric).
        Expected value is 'Microsoft.Azure.Management.Insights.Models.LocationThresholdRuleCondition'.
        """
        return pulumi.get(self, "odata_type")

    @property
    @pulumi.getter(name="dataSource")
    def data_source(self) -> Optional[Any]:
        """
        the resource from which the rule collects its data. For this type dataSource will always be of type RuleMetricDataSource.
        """
        return pulumi.get(self, "data_source")

    @property
    @pulumi.getter(name="windowSize")
    def window_size(self) -> Optional[str]:
        """
        the period of time (in ISO 8601 duration format) that is used to monitor alert activity based on the threshold. If specified then it must be between 5 minutes and 1 day.
        """
        return pulumi.get(self, "window_size")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ManagementEventAggregationConditionResponse(dict):
    """
    How the data that is collected should be combined over time.
    """
    def __init__(__self__, *,
                 operator: Optional[str] = None,
                 threshold: Optional[float] = None,
                 window_size: Optional[str] = None):
        """
        How the data that is collected should be combined over time.
        :param str operator: the condition operator.
        :param float threshold: The threshold value that activates the alert.
        :param str window_size: the period of time (in ISO 8601 duration format) that is used to monitor alert activity based on the threshold. If specified then it must be between 5 minutes and 1 day.
        """
        if operator is not None:
            pulumi.set(__self__, "operator", operator)
        if threshold is not None:
            pulumi.set(__self__, "threshold", threshold)
        if window_size is not None:
            pulumi.set(__self__, "window_size", window_size)

    @property
    @pulumi.getter
    def operator(self) -> Optional[str]:
        """
        the condition operator.
        """
        return pulumi.get(self, "operator")

    @property
    @pulumi.getter
    def threshold(self) -> Optional[float]:
        """
        The threshold value that activates the alert.
        """
        return pulumi.get(self, "threshold")

    @property
    @pulumi.getter(name="windowSize")
    def window_size(self) -> Optional[str]:
        """
        the period of time (in ISO 8601 duration format) that is used to monitor alert activity based on the threshold. If specified then it must be between 5 minutes and 1 day.
        """
        return pulumi.get(self, "window_size")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ManagementEventRuleConditionResponse(dict):
    """
    A management event rule condition.
    """
    def __init__(__self__, *,
                 odata_type: str,
                 aggregation: Optional['outputs.ManagementEventAggregationConditionResponse'] = None,
                 data_source: Optional[Any] = None):
        """
        A management event rule condition.
        :param str odata_type: specifies the type of condition. This can be one of three types: ManagementEventRuleCondition (occurrences of management events), LocationThresholdRuleCondition (based on the number of failures of a web test), and ThresholdRuleCondition (based on the threshold of a metric).
               Expected value is 'Microsoft.Azure.Management.Insights.Models.ManagementEventRuleCondition'.
        :param 'ManagementEventAggregationConditionResponseArgs' aggregation: How the data that is collected should be combined over time and when the alert is activated. Note that for management event alerts aggregation is optional – if it is not provided then any event will cause the alert to activate.
        :param Union['RuleManagementEventDataSourceResponseArgs', 'RuleMetricDataSourceResponseArgs'] data_source: the resource from which the rule collects its data. For this type dataSource will always be of type RuleMetricDataSource.
        """
        pulumi.set(__self__, "odata_type", 'Microsoft.Azure.Management.Insights.Models.ManagementEventRuleCondition')
        if aggregation is not None:
            pulumi.set(__self__, "aggregation", aggregation)
        if data_source is not None:
            pulumi.set(__self__, "data_source", data_source)

    @property
    @pulumi.getter(name="odataType")
    def odata_type(self) -> str:
        """
        specifies the type of condition. This can be one of three types: ManagementEventRuleCondition (occurrences of management events), LocationThresholdRuleCondition (based on the number of failures of a web test), and ThresholdRuleCondition (based on the threshold of a metric).
        Expected value is 'Microsoft.Azure.Management.Insights.Models.ManagementEventRuleCondition'.
        """
        return pulumi.get(self, "odata_type")

    @property
    @pulumi.getter
    def aggregation(self) -> Optional['outputs.ManagementEventAggregationConditionResponse']:
        """
        How the data that is collected should be combined over time and when the alert is activated. Note that for management event alerts aggregation is optional – if it is not provided then any event will cause the alert to activate.
        """
        return pulumi.get(self, "aggregation")

    @property
    @pulumi.getter(name="dataSource")
    def data_source(self) -> Optional[Any]:
        """
        the resource from which the rule collects its data. For this type dataSource will always be of type RuleMetricDataSource.
        """
        return pulumi.get(self, "data_source")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class RetentionPolicyResponse(dict):
    """
    Specifies the retention policy for the log.
    """
    def __init__(__self__, *,
                 days: int,
                 enabled: bool):
        """
        Specifies the retention policy for the log.
        :param int days: the number of days for the retention in days. A value of 0 will retain the events indefinitely.
        :param bool enabled: a value indicating whether the retention policy is enabled.
        """
        pulumi.set(__self__, "days", days)
        pulumi.set(__self__, "enabled", enabled)

    @property
    @pulumi.getter
    def days(self) -> int:
        """
        the number of days for the retention in days. A value of 0 will retain the events indefinitely.
        """
        return pulumi.get(self, "days")

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        a value indicating whether the retention policy is enabled.
        """
        return pulumi.get(self, "enabled")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class RuleEmailActionResponse(dict):
    """
    Specifies the action to send email when the rule condition is evaluated. The discriminator is always RuleEmailAction in this case.
    """
    def __init__(__self__, *,
                 odata_type: str,
                 custom_emails: Optional[Sequence[str]] = None,
                 send_to_service_owners: Optional[bool] = None):
        """
        Specifies the action to send email when the rule condition is evaluated. The discriminator is always RuleEmailAction in this case.
        :param str odata_type: specifies the type of the action. There are two types of actions: RuleEmailAction and RuleWebhookAction.
               Expected value is 'Microsoft.Azure.Management.Insights.Models.RuleEmailAction'.
        :param Sequence[str] custom_emails: the list of administrator's custom email addresses to notify of the activation of the alert.
        :param bool send_to_service_owners: Whether the administrators (service and co-administrators) of the service should be notified when the alert is activated.
        """
        pulumi.set(__self__, "odata_type", 'Microsoft.Azure.Management.Insights.Models.RuleEmailAction')
        if custom_emails is not None:
            pulumi.set(__self__, "custom_emails", custom_emails)
        if send_to_service_owners is not None:
            pulumi.set(__self__, "send_to_service_owners", send_to_service_owners)

    @property
    @pulumi.getter(name="odataType")
    def odata_type(self) -> str:
        """
        specifies the type of the action. There are two types of actions: RuleEmailAction and RuleWebhookAction.
        Expected value is 'Microsoft.Azure.Management.Insights.Models.RuleEmailAction'.
        """
        return pulumi.get(self, "odata_type")

    @property
    @pulumi.getter(name="customEmails")
    def custom_emails(self) -> Optional[Sequence[str]]:
        """
        the list of administrator's custom email addresses to notify of the activation of the alert.
        """
        return pulumi.get(self, "custom_emails")

    @property
    @pulumi.getter(name="sendToServiceOwners")
    def send_to_service_owners(self) -> Optional[bool]:
        """
        Whether the administrators (service and co-administrators) of the service should be notified when the alert is activated.
        """
        return pulumi.get(self, "send_to_service_owners")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class RuleManagementEventClaimsDataSourceResponse(dict):
    """
    The claims for a rule management event data source.
    """
    def __init__(__self__, *,
                 email_address: Optional[str] = None):
        """
        The claims for a rule management event data source.
        :param str email_address: the email address.
        """
        if email_address is not None:
            pulumi.set(__self__, "email_address", email_address)

    @property
    @pulumi.getter(name="emailAddress")
    def email_address(self) -> Optional[str]:
        """
        the email address.
        """
        return pulumi.get(self, "email_address")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class RuleManagementEventDataSourceResponse(dict):
    """
    A rule management event data source. The discriminator fields is always RuleManagementEventDataSource in this case.
    """
    def __init__(__self__, *,
                 odata_type: str,
                 claims: Optional['outputs.RuleManagementEventClaimsDataSourceResponse'] = None,
                 event_name: Optional[str] = None,
                 event_source: Optional[str] = None,
                 level: Optional[str] = None,
                 operation_name: Optional[str] = None,
                 resource_group_name: Optional[str] = None,
                 resource_provider_name: Optional[str] = None,
                 resource_uri: Optional[str] = None,
                 status: Optional[str] = None,
                 sub_status: Optional[str] = None):
        """
        A rule management event data source. The discriminator fields is always RuleManagementEventDataSource in this case.
        :param str odata_type: specifies the type of data source. There are two types of rule data sources: RuleMetricDataSource and RuleManagementEventDataSource
               Expected value is 'Microsoft.Azure.Management.Insights.Models.RuleManagementEventDataSource'.
        :param 'RuleManagementEventClaimsDataSourceResponseArgs' claims: the claims.
        :param str event_name: the event name.
        :param str event_source: the event source.
        :param str level: the level.
        :param str operation_name: The name of the operation that should be checked for. If no name is provided, any operation will match.
        :param str resource_group_name: the resource group name.
        :param str resource_provider_name: the resource provider name.
        :param str resource_uri: the resource identifier of the resource the rule monitors. **NOTE**: this property cannot be updated for an existing rule.
        :param str status: The status of the operation that should be checked for. If no status is provided, any status will match.
        :param str sub_status: the substatus.
        """
        pulumi.set(__self__, "odata_type", 'Microsoft.Azure.Management.Insights.Models.RuleManagementEventDataSource')
        if claims is not None:
            pulumi.set(__self__, "claims", claims)
        if event_name is not None:
            pulumi.set(__self__, "event_name", event_name)
        if event_source is not None:
            pulumi.set(__self__, "event_source", event_source)
        if level is not None:
            pulumi.set(__self__, "level", level)
        if operation_name is not None:
            pulumi.set(__self__, "operation_name", operation_name)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if resource_provider_name is not None:
            pulumi.set(__self__, "resource_provider_name", resource_provider_name)
        if resource_uri is not None:
            pulumi.set(__self__, "resource_uri", resource_uri)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if sub_status is not None:
            pulumi.set(__self__, "sub_status", sub_status)

    @property
    @pulumi.getter(name="odataType")
    def odata_type(self) -> str:
        """
        specifies the type of data source. There are two types of rule data sources: RuleMetricDataSource and RuleManagementEventDataSource
        Expected value is 'Microsoft.Azure.Management.Insights.Models.RuleManagementEventDataSource'.
        """
        return pulumi.get(self, "odata_type")

    @property
    @pulumi.getter
    def claims(self) -> Optional['outputs.RuleManagementEventClaimsDataSourceResponse']:
        """
        the claims.
        """
        return pulumi.get(self, "claims")

    @property
    @pulumi.getter(name="eventName")
    def event_name(self) -> Optional[str]:
        """
        the event name.
        """
        return pulumi.get(self, "event_name")

    @property
    @pulumi.getter(name="eventSource")
    def event_source(self) -> Optional[str]:
        """
        the event source.
        """
        return pulumi.get(self, "event_source")

    @property
    @pulumi.getter
    def level(self) -> Optional[str]:
        """
        the level.
        """
        return pulumi.get(self, "level")

    @property
    @pulumi.getter(name="operationName")
    def operation_name(self) -> Optional[str]:
        """
        The name of the operation that should be checked for. If no name is provided, any operation will match.
        """
        return pulumi.get(self, "operation_name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[str]:
        """
        the resource group name.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="resourceProviderName")
    def resource_provider_name(self) -> Optional[str]:
        """
        the resource provider name.
        """
        return pulumi.get(self, "resource_provider_name")

    @property
    @pulumi.getter(name="resourceUri")
    def resource_uri(self) -> Optional[str]:
        """
        the resource identifier of the resource the rule monitors. **NOTE**: this property cannot be updated for an existing rule.
        """
        return pulumi.get(self, "resource_uri")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        The status of the operation that should be checked for. If no status is provided, any status will match.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="subStatus")
    def sub_status(self) -> Optional[str]:
        """
        the substatus.
        """
        return pulumi.get(self, "sub_status")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class RuleMetricDataSourceResponse(dict):
    """
    A rule metric data source. The discriminator value is always RuleMetricDataSource in this case.
    """
    def __init__(__self__, *,
                 odata_type: str,
                 metric_name: Optional[str] = None,
                 resource_uri: Optional[str] = None):
        """
        A rule metric data source. The discriminator value is always RuleMetricDataSource in this case.
        :param str odata_type: specifies the type of data source. There are two types of rule data sources: RuleMetricDataSource and RuleManagementEventDataSource
               Expected value is 'Microsoft.Azure.Management.Insights.Models.RuleMetricDataSource'.
        :param str metric_name: the name of the metric that defines what the rule monitors.
        :param str resource_uri: the resource identifier of the resource the rule monitors. **NOTE**: this property cannot be updated for an existing rule.
        """
        pulumi.set(__self__, "odata_type", 'Microsoft.Azure.Management.Insights.Models.RuleMetricDataSource')
        if metric_name is not None:
            pulumi.set(__self__, "metric_name", metric_name)
        if resource_uri is not None:
            pulumi.set(__self__, "resource_uri", resource_uri)

    @property
    @pulumi.getter(name="odataType")
    def odata_type(self) -> str:
        """
        specifies the type of data source. There are two types of rule data sources: RuleMetricDataSource and RuleManagementEventDataSource
        Expected value is 'Microsoft.Azure.Management.Insights.Models.RuleMetricDataSource'.
        """
        return pulumi.get(self, "odata_type")

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> Optional[str]:
        """
        the name of the metric that defines what the rule monitors.
        """
        return pulumi.get(self, "metric_name")

    @property
    @pulumi.getter(name="resourceUri")
    def resource_uri(self) -> Optional[str]:
        """
        the resource identifier of the resource the rule monitors. **NOTE**: this property cannot be updated for an existing rule.
        """
        return pulumi.get(self, "resource_uri")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class RuleWebhookActionResponse(dict):
    """
    Specifies the action to post to service when the rule condition is evaluated. The discriminator is always RuleWebhookAction in this case.
    """
    def __init__(__self__, *,
                 odata_type: str,
                 properties: Optional[Mapping[str, str]] = None,
                 service_uri: Optional[str] = None):
        """
        Specifies the action to post to service when the rule condition is evaluated. The discriminator is always RuleWebhookAction in this case.
        :param str odata_type: specifies the type of the action. There are two types of actions: RuleEmailAction and RuleWebhookAction.
               Expected value is 'Microsoft.Azure.Management.Insights.Models.RuleWebhookAction'.
        :param Mapping[str, str] properties: the dictionary of custom properties to include with the post operation. These data are appended to the webhook payload.
        :param str service_uri: the service uri to Post the notification when the alert activates or resolves.
        """
        pulumi.set(__self__, "odata_type", 'Microsoft.Azure.Management.Insights.Models.RuleWebhookAction')
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if service_uri is not None:
            pulumi.set(__self__, "service_uri", service_uri)

    @property
    @pulumi.getter(name="odataType")
    def odata_type(self) -> str:
        """
        specifies the type of the action. There are two types of actions: RuleEmailAction and RuleWebhookAction.
        Expected value is 'Microsoft.Azure.Management.Insights.Models.RuleWebhookAction'.
        """
        return pulumi.get(self, "odata_type")

    @property
    @pulumi.getter
    def properties(self) -> Optional[Mapping[str, str]]:
        """
        the dictionary of custom properties to include with the post operation. These data are appended to the webhook payload.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter(name="serviceUri")
    def service_uri(self) -> Optional[str]:
        """
        the service uri to Post the notification when the alert activates or resolves.
        """
        return pulumi.get(self, "service_uri")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ThresholdRuleConditionResponse(dict):
    """
    A rule condition based on a metric crossing a threshold.
    """
    def __init__(__self__, *,
                 odata_type: str,
                 operator: str,
                 threshold: float,
                 data_source: Optional[Any] = None,
                 time_aggregation: Optional[str] = None,
                 window_size: Optional[str] = None):
        """
        A rule condition based on a metric crossing a threshold.
        :param str odata_type: specifies the type of condition. This can be one of three types: ManagementEventRuleCondition (occurrences of management events), LocationThresholdRuleCondition (based on the number of failures of a web test), and ThresholdRuleCondition (based on the threshold of a metric).
               Expected value is 'Microsoft.Azure.Management.Insights.Models.ThresholdRuleCondition'.
        :param str operator: the operator used to compare the data and the threshold.
        :param float threshold: the threshold value that activates the alert.
        :param Union['RuleManagementEventDataSourceResponseArgs', 'RuleMetricDataSourceResponseArgs'] data_source: the resource from which the rule collects its data. For this type dataSource will always be of type RuleMetricDataSource.
        :param str time_aggregation: the time aggregation operator. How the data that are collected should be combined over time. The default value is the PrimaryAggregationType of the Metric.
        :param str window_size: the period of time (in ISO 8601 duration format) that is used to monitor alert activity based on the threshold. If specified then it must be between 5 minutes and 1 day.
        """
        pulumi.set(__self__, "odata_type", 'Microsoft.Azure.Management.Insights.Models.ThresholdRuleCondition')
        pulumi.set(__self__, "operator", operator)
        pulumi.set(__self__, "threshold", threshold)
        if data_source is not None:
            pulumi.set(__self__, "data_source", data_source)
        if time_aggregation is not None:
            pulumi.set(__self__, "time_aggregation", time_aggregation)
        if window_size is not None:
            pulumi.set(__self__, "window_size", window_size)

    @property
    @pulumi.getter(name="odataType")
    def odata_type(self) -> str:
        """
        specifies the type of condition. This can be one of three types: ManagementEventRuleCondition (occurrences of management events), LocationThresholdRuleCondition (based on the number of failures of a web test), and ThresholdRuleCondition (based on the threshold of a metric).
        Expected value is 'Microsoft.Azure.Management.Insights.Models.ThresholdRuleCondition'.
        """
        return pulumi.get(self, "odata_type")

    @property
    @pulumi.getter
    def operator(self) -> str:
        """
        the operator used to compare the data and the threshold.
        """
        return pulumi.get(self, "operator")

    @property
    @pulumi.getter
    def threshold(self) -> float:
        """
        the threshold value that activates the alert.
        """
        return pulumi.get(self, "threshold")

    @property
    @pulumi.getter(name="dataSource")
    def data_source(self) -> Optional[Any]:
        """
        the resource from which the rule collects its data. For this type dataSource will always be of type RuleMetricDataSource.
        """
        return pulumi.get(self, "data_source")

    @property
    @pulumi.getter(name="timeAggregation")
    def time_aggregation(self) -> Optional[str]:
        """
        the time aggregation operator. How the data that are collected should be combined over time. The default value is the PrimaryAggregationType of the Metric.
        """
        return pulumi.get(self, "time_aggregation")

    @property
    @pulumi.getter(name="windowSize")
    def window_size(self) -> Optional[str]:
        """
        the period of time (in ISO 8601 duration format) that is used to monitor alert activity based on the threshold. If specified then it must be between 5 minutes and 1 day.
        """
        return pulumi.get(self, "window_size")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


