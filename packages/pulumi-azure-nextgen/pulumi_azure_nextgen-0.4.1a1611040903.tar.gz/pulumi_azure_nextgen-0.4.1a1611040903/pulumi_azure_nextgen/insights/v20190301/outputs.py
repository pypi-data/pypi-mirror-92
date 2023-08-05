# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'ArmRoleReceiverResponse',
    'AutomationRunbookReceiverResponse',
    'AzureAppPushReceiverResponse',
    'AzureFunctionReceiverResponse',
    'EmailReceiverResponse',
    'ItsmReceiverResponse',
    'LogicAppReceiverResponse',
    'SmsReceiverResponse',
    'VoiceReceiverResponse',
    'WebhookReceiverResponse',
]

@pulumi.output_type
class ArmRoleReceiverResponse(dict):
    """
    An arm role receiver.
    """
    def __init__(__self__, *,
                 name: str,
                 role_id: str,
                 use_common_alert_schema: bool):
        """
        An arm role receiver.
        :param str name: The name of the arm role receiver. Names must be unique across all receivers within an action group.
        :param str role_id: The arm role id.
        :param bool use_common_alert_schema: Indicates whether to use common alert schema.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "role_id", role_id)
        pulumi.set(__self__, "use_common_alert_schema", use_common_alert_schema)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the arm role receiver. Names must be unique across all receivers within an action group.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="roleId")
    def role_id(self) -> str:
        """
        The arm role id.
        """
        return pulumi.get(self, "role_id")

    @property
    @pulumi.getter(name="useCommonAlertSchema")
    def use_common_alert_schema(self) -> bool:
        """
        Indicates whether to use common alert schema.
        """
        return pulumi.get(self, "use_common_alert_schema")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class AutomationRunbookReceiverResponse(dict):
    """
    The Azure Automation Runbook notification receiver.
    """
    def __init__(__self__, *,
                 automation_account_id: str,
                 is_global_runbook: bool,
                 runbook_name: str,
                 use_common_alert_schema: bool,
                 webhook_resource_id: str,
                 name: Optional[str] = None,
                 service_uri: Optional[str] = None):
        """
        The Azure Automation Runbook notification receiver.
        :param str automation_account_id: The Azure automation account Id which holds this runbook and authenticate to Azure resource.
        :param bool is_global_runbook: Indicates whether this instance is global runbook.
        :param str runbook_name: The name for this runbook.
        :param bool use_common_alert_schema: Indicates whether to use common alert schema.
        :param str webhook_resource_id: The resource id for webhook linked to this runbook.
        :param str name: Indicates name of the webhook.
        :param str service_uri: The URI where webhooks should be sent.
        """
        pulumi.set(__self__, "automation_account_id", automation_account_id)
        pulumi.set(__self__, "is_global_runbook", is_global_runbook)
        pulumi.set(__self__, "runbook_name", runbook_name)
        pulumi.set(__self__, "use_common_alert_schema", use_common_alert_schema)
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
    @pulumi.getter(name="useCommonAlertSchema")
    def use_common_alert_schema(self) -> bool:
        """
        Indicates whether to use common alert schema.
        """
        return pulumi.get(self, "use_common_alert_schema")

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
                 name: str,
                 use_common_alert_schema: bool):
        """
        An azure function receiver.
        :param str function_app_resource_id: The azure resource id of the function app.
        :param str function_name: The function name in the function app.
        :param str http_trigger_url: The http trigger url where http request sent to.
        :param str name: The name of the azure function receiver. Names must be unique across all receivers within an action group.
        :param bool use_common_alert_schema: Indicates whether to use common alert schema.
        """
        pulumi.set(__self__, "function_app_resource_id", function_app_resource_id)
        pulumi.set(__self__, "function_name", function_name)
        pulumi.set(__self__, "http_trigger_url", http_trigger_url)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "use_common_alert_schema", use_common_alert_schema)

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

    @property
    @pulumi.getter(name="useCommonAlertSchema")
    def use_common_alert_schema(self) -> bool:
        """
        Indicates whether to use common alert schema.
        """
        return pulumi.get(self, "use_common_alert_schema")

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
                 status: str,
                 use_common_alert_schema: bool):
        """
        An email receiver.
        :param str email_address: The email address of this receiver.
        :param str name: The name of the email receiver. Names must be unique across all receivers within an action group.
        :param str status: The receiver status of the e-mail.
        :param bool use_common_alert_schema: Indicates whether to use common alert schema.
        """
        pulumi.set(__self__, "email_address", email_address)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "status", status)
        pulumi.set(__self__, "use_common_alert_schema", use_common_alert_schema)

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

    @property
    @pulumi.getter(name="useCommonAlertSchema")
    def use_common_alert_schema(self) -> bool:
        """
        Indicates whether to use common alert schema.
        """
        return pulumi.get(self, "use_common_alert_schema")

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
                 resource_id: str,
                 use_common_alert_schema: bool):
        """
        A logic app receiver.
        :param str callback_url: The callback url where http request sent to.
        :param str name: The name of the logic app receiver. Names must be unique across all receivers within an action group.
        :param str resource_id: The azure resource id of the logic app receiver.
        :param bool use_common_alert_schema: Indicates whether to use common alert schema.
        """
        pulumi.set(__self__, "callback_url", callback_url)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "resource_id", resource_id)
        pulumi.set(__self__, "use_common_alert_schema", use_common_alert_schema)

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

    @property
    @pulumi.getter(name="useCommonAlertSchema")
    def use_common_alert_schema(self) -> bool:
        """
        Indicates whether to use common alert schema.
        """
        return pulumi.get(self, "use_common_alert_schema")

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
                 service_uri: str,
                 use_common_alert_schema: bool):
        """
        A webhook receiver.
        :param str name: The name of the webhook receiver. Names must be unique across all receivers within an action group.
        :param str service_uri: The URI where webhooks should be sent.
        :param bool use_common_alert_schema: Indicates whether to use common alert schema.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "service_uri", service_uri)
        pulumi.set(__self__, "use_common_alert_schema", use_common_alert_schema)

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

    @property
    @pulumi.getter(name="useCommonAlertSchema")
    def use_common_alert_schema(self) -> bool:
        """
        Indicates whether to use common alert schema.
        """
        return pulumi.get(self, "use_common_alert_schema")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


