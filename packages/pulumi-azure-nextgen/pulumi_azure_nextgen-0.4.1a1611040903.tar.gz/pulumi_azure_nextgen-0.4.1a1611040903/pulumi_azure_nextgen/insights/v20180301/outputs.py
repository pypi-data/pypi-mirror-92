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
    'AutomationRunbookReceiverResponse',
    'AzureAppPushReceiverResponse',
    'AzureFunctionReceiverResponse',
    'DynamicMetricCriteriaResponse',
    'DynamicThresholdFailingPeriodsResponse',
    'EmailReceiverResponse',
    'ItsmReceiverResponse',
    'LogicAppReceiverResponse',
    'MetricAlertActionResponse',
    'MetricAlertMultipleResourceMultipleMetricCriteriaResponse',
    'MetricAlertSingleResourceMultipleMetricCriteriaResponse',
    'MetricCriteriaResponse',
    'MetricDimensionResponse',
    'SmsReceiverResponse',
    'VoiceReceiverResponse',
    'WebhookReceiverResponse',
    'WebtestLocationAvailabilityCriteriaResponse',
]

@pulumi.output_type
class AutomationRunbookReceiverResponse(dict):
    """
    The Azure Automation Runbook notification receiver.
    """
    def __init__(__self__, *,
                 automation_account_id: str,
                 is_global_runbook: bool,
                 runbook_name: str,
                 webhook_resource_id: str,
                 name: Optional[str] = None,
                 service_uri: Optional[str] = None):
        """
        The Azure Automation Runbook notification receiver.
        :param str automation_account_id: The Azure automation account Id which holds this runbook and authenticate to Azure resource.
        :param bool is_global_runbook: Indicates whether this instance is global runbook.
        :param str runbook_name: The name for this runbook.
        :param str webhook_resource_id: The resource id for webhook linked to this runbook.
        :param str name: Indicates name of the webhook.
        :param str service_uri: The URI where webhooks should be sent.
        """
        pulumi.set(__self__, "automation_account_id", automation_account_id)
        pulumi.set(__self__, "is_global_runbook", is_global_runbook)
        pulumi.set(__self__, "runbook_name", runbook_name)
        pulumi.set(__self__, "webhook_resource_id", webhook_resource_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if service_uri is not None:
            pulumi.set(__self__, "service_uri", service_uri)

    @property
    @pulumi.getter(name="automationAccountId")
    def automation_account_id(self) -> str:
        """
        The Azure automation account Id which holds this runbook and authenticate to Azure resource.
        """
        return pulumi.get(self, "automation_account_id")

    @property
    @pulumi.getter(name="isGlobalRunbook")
    def is_global_runbook(self) -> bool:
        """
        Indicates whether this instance is global runbook.
        """
        return pulumi.get(self, "is_global_runbook")

    @property
    @pulumi.getter(name="runbookName")
    def runbook_name(self) -> str:
        """
        The name for this runbook.
        """
        return pulumi.get(self, "runbook_name")

    @property
    @pulumi.getter(name="webhookResourceId")
    def webhook_resource_id(self) -> str:
        """
        The resource id for webhook linked to this runbook.
        """
        return pulumi.get(self, "webhook_resource_id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Indicates name of the webhook.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="serviceUri")
    def service_uri(self) -> Optional[str]:
        """
        The URI where webhooks should be sent.
        """
        return pulumi.get(self, "service_uri")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class AzureAppPushReceiverResponse(dict):
    """
    The Azure mobile App push notification receiver.
    """
    def __init__(__self__, *,
                 email_address: str,
                 name: str):
        """
        The Azure mobile App push notification receiver.
        :param str email_address: The email address registered for the Azure mobile app.
        :param str name: The name of the Azure mobile app push receiver. Names must be unique across all receivers within an action group.
        """
        pulumi.set(__self__, "email_address", email_address)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="emailAddress")
    def email_address(self) -> str:
        """
        The email address registered for the Azure mobile app.
        """
        return pulumi.get(self, "email_address")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the Azure mobile app push receiver. Names must be unique across all receivers within an action group.
        """
        return pulumi.get(self, "name")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class AzureFunctionReceiverResponse(dict):
    """
    An azure function receiver.
    """
    def __init__(__self__, *,
                 function_app_resource_id: str,
                 function_name: str,
                 http_trigger_url: str,
                 name: str):
        """
        An azure function receiver.
        :param str function_app_resource_id: The azure resource id of the function app.
        :param str function_name: The function name in the function app.
        :param str http_trigger_url: The http trigger url where http request sent to.
        :param str name: The name of the azure function receiver. Names must be unique across all receivers within an action group.
        """
        pulumi.set(__self__, "function_app_resource_id", function_app_resource_id)
        pulumi.set(__self__, "function_name", function_name)
        pulumi.set(__self__, "http_trigger_url", http_trigger_url)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="functionAppResourceId")
    def function_app_resource_id(self) -> str:
        """
        The azure resource id of the function app.
        """
        return pulumi.get(self, "function_app_resource_id")

    @property
    @pulumi.getter(name="functionName")
    def function_name(self) -> str:
        """
        The function name in the function app.
        """
        return pulumi.get(self, "function_name")

    @property
    @pulumi.getter(name="httpTriggerUrl")
    def http_trigger_url(self) -> str:
        """
        The http trigger url where http request sent to.
        """
        return pulumi.get(self, "http_trigger_url")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the azure function receiver. Names must be unique across all receivers within an action group.
        """
        return pulumi.get(self, "name")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class DynamicMetricCriteriaResponse(dict):
    """
    Criterion for dynamic threshold.
    """
    def __init__(__self__, *,
                 alert_sensitivity: str,
                 criterion_type: str,
                 failing_periods: 'outputs.DynamicThresholdFailingPeriodsResponse',
                 metric_name: str,
                 name: str,
                 operator: str,
                 time_aggregation: str,
                 dimensions: Optional[Sequence['outputs.MetricDimensionResponse']] = None,
                 ignore_data_before: Optional[str] = None,
                 metric_namespace: Optional[str] = None,
                 skip_metric_validation: Optional[bool] = None):
        """
        Criterion for dynamic threshold.
        :param str alert_sensitivity: The extent of deviation required to trigger an alert. This will affect how tight the threshold is to the metric series pattern.
        :param str criterion_type: Specifies the type of threshold criteria
               Expected value is 'DynamicThresholdCriterion'.
        :param 'DynamicThresholdFailingPeriodsResponseArgs' failing_periods: The minimum number of violations required within the selected lookback time window required to raise an alert.
        :param str metric_name: Name of the metric.
        :param str name: Name of the criteria.
        :param str operator: The operator used to compare the metric value against the threshold.
        :param str time_aggregation: the criteria time aggregation types.
        :param Sequence['MetricDimensionResponseArgs'] dimensions: List of dimension conditions.
        :param str ignore_data_before: Use this option to set the date from which to start learning the metric historical data and calculate the dynamic thresholds (in ISO8601 format)
        :param str metric_namespace: Namespace of the metric.
        :param bool skip_metric_validation: Allows creating an alert rule on a custom metric that isn't yet emitted, by causing the metric validation to be skipped.
        """
        pulumi.set(__self__, "alert_sensitivity", alert_sensitivity)
        pulumi.set(__self__, "criterion_type", 'DynamicThresholdCriterion')
        pulumi.set(__self__, "failing_periods", failing_periods)
        pulumi.set(__self__, "metric_name", metric_name)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "operator", operator)
        pulumi.set(__self__, "time_aggregation", time_aggregation)
        if dimensions is not None:
            pulumi.set(__self__, "dimensions", dimensions)
        if ignore_data_before is not None:
            pulumi.set(__self__, "ignore_data_before", ignore_data_before)
        if metric_namespace is not None:
            pulumi.set(__self__, "metric_namespace", metric_namespace)
        if skip_metric_validation is not None:
            pulumi.set(__self__, "skip_metric_validation", skip_metric_validation)

    @property
    @pulumi.getter(name="alertSensitivity")
    def alert_sensitivity(self) -> str:
        """
        The extent of deviation required to trigger an alert. This will affect how tight the threshold is to the metric series pattern.
        """
        return pulumi.get(self, "alert_sensitivity")

    @property
    @pulumi.getter(name="criterionType")
    def criterion_type(self) -> str:
        """
        Specifies the type of threshold criteria
        Expected value is 'DynamicThresholdCriterion'.
        """
        return pulumi.get(self, "criterion_type")

    @property
    @pulumi.getter(name="failingPeriods")
    def failing_periods(self) -> 'outputs.DynamicThresholdFailingPeriodsResponse':
        """
        The minimum number of violations required within the selected lookback time window required to raise an alert.
        """
        return pulumi.get(self, "failing_periods")

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> str:
        """
        Name of the metric.
        """
        return pulumi.get(self, "metric_name")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the criteria.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def operator(self) -> str:
        """
        The operator used to compare the metric value against the threshold.
        """
        return pulumi.get(self, "operator")

    @property
    @pulumi.getter(name="timeAggregation")
    def time_aggregation(self) -> str:
        """
        the criteria time aggregation types.
        """
        return pulumi.get(self, "time_aggregation")

    @property
    @pulumi.getter
    def dimensions(self) -> Optional[Sequence['outputs.MetricDimensionResponse']]:
        """
        List of dimension conditions.
        """
        return pulumi.get(self, "dimensions")

    @property
    @pulumi.getter(name="ignoreDataBefore")
    def ignore_data_before(self) -> Optional[str]:
        """
        Use this option to set the date from which to start learning the metric historical data and calculate the dynamic thresholds (in ISO8601 format)
        """
        return pulumi.get(self, "ignore_data_before")

    @property
    @pulumi.getter(name="metricNamespace")
    def metric_namespace(self) -> Optional[str]:
        """
        Namespace of the metric.
        """
        return pulumi.get(self, "metric_namespace")

    @property
    @pulumi.getter(name="skipMetricValidation")
    def skip_metric_validation(self) -> Optional[bool]:
        """
        Allows creating an alert rule on a custom metric that isn't yet emitted, by causing the metric validation to be skipped.
        """
        return pulumi.get(self, "skip_metric_validation")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class DynamicThresholdFailingPeriodsResponse(dict):
    """
    The minimum number of violations required within the selected lookback time window required to raise an alert.
    """
    def __init__(__self__, *,
                 min_failing_periods_to_alert: float,
                 number_of_evaluation_periods: float):
        """
        The minimum number of violations required within the selected lookback time window required to raise an alert.
        :param float min_failing_periods_to_alert: The number of violations to trigger an alert. Should be smaller or equal to numberOfEvaluationPeriods.
        :param float number_of_evaluation_periods: The number of aggregated lookback points. The lookback time window is calculated based on the aggregation granularity (windowSize) and the selected number of aggregated points.
        """
        pulumi.set(__self__, "min_failing_periods_to_alert", min_failing_periods_to_alert)
        pulumi.set(__self__, "number_of_evaluation_periods", number_of_evaluation_periods)

    @property
    @pulumi.getter(name="minFailingPeriodsToAlert")
    def min_failing_periods_to_alert(self) -> float:
        """
        The number of violations to trigger an alert. Should be smaller or equal to numberOfEvaluationPeriods.
        """
        return pulumi.get(self, "min_failing_periods_to_alert")

    @property
    @pulumi.getter(name="numberOfEvaluationPeriods")
    def number_of_evaluation_periods(self) -> float:
        """
        The number of aggregated lookback points. The lookback time window is calculated based on the aggregation granularity (windowSize) and the selected number of aggregated points.
        """
        return pulumi.get(self, "number_of_evaluation_periods")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class EmailReceiverResponse(dict):
    """
    An email receiver.
    """
    def __init__(__self__, *,
                 email_address: str,
                 name: str,
                 status: str):
        """
        An email receiver.
        :param str email_address: The email address of this receiver.
        :param str name: The name of the email receiver. Names must be unique across all receivers within an action group.
        :param str status: The receiver status of the e-mail.
        """
        pulumi.set(__self__, "email_address", email_address)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="emailAddress")
    def email_address(self) -> str:
        """
        The email address of this receiver.
        """
        return pulumi.get(self, "email_address")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the email receiver. Names must be unique across all receivers within an action group.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The receiver status of the e-mail.
        """
        return pulumi.get(self, "status")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ItsmReceiverResponse(dict):
    """
    An Itsm receiver.
    """
    def __init__(__self__, *,
                 connection_id: str,
                 name: str,
                 region: str,
                 ticket_configuration: str,
                 workspace_id: str):
        """
        An Itsm receiver.
        :param str connection_id: Unique identification of ITSM connection among multiple defined in above workspace.
        :param str name: The name of the Itsm receiver. Names must be unique across all receivers within an action group.
        :param str region: Region in which workspace resides. Supported values:'centralindia','japaneast','southeastasia','australiasoutheast','uksouth','westcentralus','canadacentral','eastus','westeurope'
        :param str ticket_configuration: JSON blob for the configurations of the ITSM action. CreateMultipleWorkItems option will be part of this blob as well.
        :param str workspace_id: OMS LA instance identifier.
        """
        pulumi.set(__self__, "connection_id", connection_id)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "region", region)
        pulumi.set(__self__, "ticket_configuration", ticket_configuration)
        pulumi.set(__self__, "workspace_id", workspace_id)

    @property
    @pulumi.getter(name="connectionId")
    def connection_id(self) -> str:
        """
        Unique identification of ITSM connection among multiple defined in above workspace.
        """
        return pulumi.get(self, "connection_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the Itsm receiver. Names must be unique across all receivers within an action group.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def region(self) -> str:
        """
        Region in which workspace resides. Supported values:'centralindia','japaneast','southeastasia','australiasoutheast','uksouth','westcentralus','canadacentral','eastus','westeurope'
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="ticketConfiguration")
    def ticket_configuration(self) -> str:
        """
        JSON blob for the configurations of the ITSM action. CreateMultipleWorkItems option will be part of this blob as well.
        """
        return pulumi.get(self, "ticket_configuration")

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> str:
        """
        OMS LA instance identifier.
        """
        return pulumi.get(self, "workspace_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class LogicAppReceiverResponse(dict):
    """
    A logic app receiver.
    """
    def __init__(__self__, *,
                 callback_url: str,
                 name: str,
                 resource_id: str):
        """
        A logic app receiver.
        :param str callback_url: The callback url where http request sent to.
        :param str name: The name of the logic app receiver. Names must be unique across all receivers within an action group.
        :param str resource_id: The azure resource id of the logic app receiver.
        """
        pulumi.set(__self__, "callback_url", callback_url)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="callbackUrl")
    def callback_url(self) -> str:
        """
        The callback url where http request sent to.
        """
        return pulumi.get(self, "callback_url")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the logic app receiver. Names must be unique across all receivers within an action group.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> str:
        """
        The azure resource id of the logic app receiver.
        """
        return pulumi.get(self, "resource_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class MetricAlertActionResponse(dict):
    """
    An alert action.
    """
    def __init__(__self__, *,
                 action_group_id: Optional[str] = None,
                 web_hook_properties: Optional[Mapping[str, str]] = None):
        """
        An alert action.
        :param str action_group_id: the id of the action group to use.
        :param Mapping[str, str] web_hook_properties: This field allows specifying custom properties, which would be appended to the alert payload sent as input to the webhook.
        """
        if action_group_id is not None:
            pulumi.set(__self__, "action_group_id", action_group_id)
        if web_hook_properties is not None:
            pulumi.set(__self__, "web_hook_properties", web_hook_properties)

    @property
    @pulumi.getter(name="actionGroupId")
    def action_group_id(self) -> Optional[str]:
        """
        the id of the action group to use.
        """
        return pulumi.get(self, "action_group_id")

    @property
    @pulumi.getter(name="webHookProperties")
    def web_hook_properties(self) -> Optional[Mapping[str, str]]:
        """
        This field allows specifying custom properties, which would be appended to the alert payload sent as input to the webhook.
        """
        return pulumi.get(self, "web_hook_properties")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class MetricAlertMultipleResourceMultipleMetricCriteriaResponse(dict):
    """
    Specifies the metric alert criteria for multiple resource that has multiple metric criteria.
    """
    def __init__(__self__, *,
                 odata_type: str,
                 all_of: Optional[Sequence[Any]] = None):
        """
        Specifies the metric alert criteria for multiple resource that has multiple metric criteria.
        :param str odata_type: specifies the type of the alert criteria.
               Expected value is 'Microsoft.Azure.Monitor.MultipleResourceMultipleMetricCriteria'.
        :param Sequence[Union['DynamicMetricCriteriaResponseArgs', 'MetricCriteriaResponseArgs']] all_of: the list of multiple metric criteria for this 'all of' operation. 
        """
        pulumi.set(__self__, "odata_type", 'Microsoft.Azure.Monitor.MultipleResourceMultipleMetricCriteria')
        if all_of is not None:
            pulumi.set(__self__, "all_of", all_of)

    @property
    @pulumi.getter(name="odataType")
    def odata_type(self) -> str:
        """
        specifies the type of the alert criteria.
        Expected value is 'Microsoft.Azure.Monitor.MultipleResourceMultipleMetricCriteria'.
        """
        return pulumi.get(self, "odata_type")

    @property
    @pulumi.getter(name="allOf")
    def all_of(self) -> Optional[Sequence[Any]]:
        """
        the list of multiple metric criteria for this 'all of' operation. 
        """
        return pulumi.get(self, "all_of")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class MetricAlertSingleResourceMultipleMetricCriteriaResponse(dict):
    """
    Specifies the metric alert criteria for a single resource that has multiple metric criteria.
    """
    def __init__(__self__, *,
                 odata_type: str,
                 all_of: Optional[Sequence['outputs.MetricCriteriaResponse']] = None):
        """
        Specifies the metric alert criteria for a single resource that has multiple metric criteria.
        :param str odata_type: specifies the type of the alert criteria.
               Expected value is 'Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria'.
        :param Sequence['MetricCriteriaResponseArgs'] all_of: The list of metric criteria for this 'all of' operation. 
        """
        pulumi.set(__self__, "odata_type", 'Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria')
        if all_of is not None:
            pulumi.set(__self__, "all_of", all_of)

    @property
    @pulumi.getter(name="odataType")
    def odata_type(self) -> str:
        """
        specifies the type of the alert criteria.
        Expected value is 'Microsoft.Azure.Monitor.SingleResourceMultipleMetricCriteria'.
        """
        return pulumi.get(self, "odata_type")

    @property
    @pulumi.getter(name="allOf")
    def all_of(self) -> Optional[Sequence['outputs.MetricCriteriaResponse']]:
        """
        The list of metric criteria for this 'all of' operation. 
        """
        return pulumi.get(self, "all_of")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class MetricCriteriaResponse(dict):
    """
    Criterion to filter metrics.
    """
    def __init__(__self__, *,
                 criterion_type: str,
                 metric_name: str,
                 name: str,
                 operator: str,
                 threshold: float,
                 time_aggregation: str,
                 dimensions: Optional[Sequence['outputs.MetricDimensionResponse']] = None,
                 metric_namespace: Optional[str] = None,
                 skip_metric_validation: Optional[bool] = None):
        """
        Criterion to filter metrics.
        :param str criterion_type: Specifies the type of threshold criteria
               Expected value is 'StaticThresholdCriterion'.
        :param str metric_name: Name of the metric.
        :param str name: Name of the criteria.
        :param str operator: the criteria operator.
        :param float threshold: the criteria threshold value that activates the alert.
        :param str time_aggregation: the criteria time aggregation types.
        :param Sequence['MetricDimensionResponseArgs'] dimensions: List of dimension conditions.
        :param str metric_namespace: Namespace of the metric.
        :param bool skip_metric_validation: Allows creating an alert rule on a custom metric that isn't yet emitted, by causing the metric validation to be skipped.
        """
        pulumi.set(__self__, "criterion_type", 'StaticThresholdCriterion')
        pulumi.set(__self__, "metric_name", metric_name)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "operator", operator)
        pulumi.set(__self__, "threshold", threshold)
        pulumi.set(__self__, "time_aggregation", time_aggregation)
        if dimensions is not None:
            pulumi.set(__self__, "dimensions", dimensions)
        if metric_namespace is not None:
            pulumi.set(__self__, "metric_namespace", metric_namespace)
        if skip_metric_validation is not None:
            pulumi.set(__self__, "skip_metric_validation", skip_metric_validation)

    @property
    @pulumi.getter(name="criterionType")
    def criterion_type(self) -> str:
        """
        Specifies the type of threshold criteria
        Expected value is 'StaticThresholdCriterion'.
        """
        return pulumi.get(self, "criterion_type")

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> str:
        """
        Name of the metric.
        """
        return pulumi.get(self, "metric_name")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the criteria.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def operator(self) -> str:
        """
        the criteria operator.
        """
        return pulumi.get(self, "operator")

    @property
    @pulumi.getter
    def threshold(self) -> float:
        """
        the criteria threshold value that activates the alert.
        """
        return pulumi.get(self, "threshold")

    @property
    @pulumi.getter(name="timeAggregation")
    def time_aggregation(self) -> str:
        """
        the criteria time aggregation types.
        """
        return pulumi.get(self, "time_aggregation")

    @property
    @pulumi.getter
    def dimensions(self) -> Optional[Sequence['outputs.MetricDimensionResponse']]:
        """
        List of dimension conditions.
        """
        return pulumi.get(self, "dimensions")

    @property
    @pulumi.getter(name="metricNamespace")
    def metric_namespace(self) -> Optional[str]:
        """
        Namespace of the metric.
        """
        return pulumi.get(self, "metric_namespace")

    @property
    @pulumi.getter(name="skipMetricValidation")
    def skip_metric_validation(self) -> Optional[bool]:
        """
        Allows creating an alert rule on a custom metric that isn't yet emitted, by causing the metric validation to be skipped.
        """
        return pulumi.get(self, "skip_metric_validation")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class MetricDimensionResponse(dict):
    """
    Specifies a metric dimension.
    """
    def __init__(__self__, *,
                 name: str,
                 operator: str,
                 values: Sequence[str]):
        """
        Specifies a metric dimension.
        :param str name: Name of the dimension.
        :param str operator: the dimension operator. Only 'Include' and 'Exclude' are supported
        :param Sequence[str] values: list of dimension values.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "operator", operator)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the dimension.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def operator(self) -> str:
        """
        the dimension operator. Only 'Include' and 'Exclude' are supported
        """
        return pulumi.get(self, "operator")

    @property
    @pulumi.getter
    def values(self) -> Sequence[str]:
        """
        list of dimension values.
        """
        return pulumi.get(self, "values")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class SmsReceiverResponse(dict):
    """
    An SMS receiver.
    """
    def __init__(__self__, *,
                 country_code: str,
                 name: str,
                 phone_number: str,
                 status: str):
        """
        An SMS receiver.
        :param str country_code: The country code of the SMS receiver.
        :param str name: The name of the SMS receiver. Names must be unique across all receivers within an action group.
        :param str phone_number: The phone number of the SMS receiver.
        :param str status: The status of the receiver.
        """
        pulumi.set(__self__, "country_code", country_code)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "phone_number", phone_number)
        pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="countryCode")
    def country_code(self) -> str:
        """
        The country code of the SMS receiver.
        """
        return pulumi.get(self, "country_code")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the SMS receiver. Names must be unique across all receivers within an action group.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="phoneNumber")
    def phone_number(self) -> str:
        """
        The phone number of the SMS receiver.
        """
        return pulumi.get(self, "phone_number")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The status of the receiver.
        """
        return pulumi.get(self, "status")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class VoiceReceiverResponse(dict):
    """
    A voice receiver.
    """
    def __init__(__self__, *,
                 country_code: str,
                 name: str,
                 phone_number: str):
        """
        A voice receiver.
        :param str country_code: The country code of the voice receiver.
        :param str name: The name of the voice receiver. Names must be unique across all receivers within an action group.
        :param str phone_number: The phone number of the voice receiver.
        """
        pulumi.set(__self__, "country_code", country_code)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "phone_number", phone_number)

    @property
    @pulumi.getter(name="countryCode")
    def country_code(self) -> str:
        """
        The country code of the voice receiver.
        """
        return pulumi.get(self, "country_code")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the voice receiver. Names must be unique across all receivers within an action group.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="phoneNumber")
    def phone_number(self) -> str:
        """
        The phone number of the voice receiver.
        """
        return pulumi.get(self, "phone_number")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class WebhookReceiverResponse(dict):
    """
    A webhook receiver.
    """
    def __init__(__self__, *,
                 name: str,
                 service_uri: str):
        """
        A webhook receiver.
        :param str name: The name of the webhook receiver. Names must be unique across all receivers within an action group.
        :param str service_uri: The URI where webhooks should be sent.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "service_uri", service_uri)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the webhook receiver. Names must be unique across all receivers within an action group.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="serviceUri")
    def service_uri(self) -> str:
        """
        The URI where webhooks should be sent.
        """
        return pulumi.get(self, "service_uri")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class WebtestLocationAvailabilityCriteriaResponse(dict):
    """
    Specifies the metric alert rule criteria for a web test resource.
    """
    def __init__(__self__, *,
                 component_id: str,
                 failed_location_count: float,
                 odata_type: str,
                 web_test_id: str):
        """
        Specifies the metric alert rule criteria for a web test resource.
        :param str component_id: The Application Insights resource Id.
        :param float failed_location_count: The number of failed locations.
        :param str odata_type: specifies the type of the alert criteria.
               Expected value is 'Microsoft.Azure.Monitor.WebtestLocationAvailabilityCriteria'.
        :param str web_test_id: The Application Insights web test Id.
        """
        pulumi.set(__self__, "component_id", component_id)
        pulumi.set(__self__, "failed_location_count", failed_location_count)
        pulumi.set(__self__, "odata_type", 'Microsoft.Azure.Monitor.WebtestLocationAvailabilityCriteria')
        pulumi.set(__self__, "web_test_id", web_test_id)

    @property
    @pulumi.getter(name="componentId")
    def component_id(self) -> str:
        """
        The Application Insights resource Id.
        """
        return pulumi.get(self, "component_id")

    @property
    @pulumi.getter(name="failedLocationCount")
    def failed_location_count(self) -> float:
        """
        The number of failed locations.
        """
        return pulumi.get(self, "failed_location_count")

    @property
    @pulumi.getter(name="odataType")
    def odata_type(self) -> str:
        """
        specifies the type of the alert criteria.
        Expected value is 'Microsoft.Azure.Monitor.WebtestLocationAvailabilityCriteria'.
        """
        return pulumi.get(self, "odata_type")

    @property
    @pulumi.getter(name="webTestId")
    def web_test_id(self) -> str:
        """
        The Application Insights web test Id.
        """
        return pulumi.get(self, "web_test_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


