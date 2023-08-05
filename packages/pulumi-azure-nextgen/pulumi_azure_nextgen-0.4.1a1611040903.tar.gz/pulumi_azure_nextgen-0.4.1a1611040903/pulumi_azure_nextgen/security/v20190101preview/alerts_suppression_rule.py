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
from ._inputs import *

__all__ = ['AlertsSuppressionRule']


class AlertsSuppressionRule(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 alert_type: Optional[pulumi.Input[str]] = None,
                 alerts_suppression_rule_name: Optional[pulumi.Input[str]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 expiration_date_utc: Optional[pulumi.Input[str]] = None,
                 reason: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[Union[str, 'RuleState']]] = None,
                 suppression_alerts_scope: Optional[pulumi.Input[pulumi.InputType['SuppressionAlertsScopeArgs']]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Describes the suppression rule

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] alert_type: Type of the alert to automatically suppress. For all alert types, use '*'
        :param pulumi.Input[str] alerts_suppression_rule_name: The unique name of the suppression alert rule
        :param pulumi.Input[str] comment: Any comment regarding the rule
        :param pulumi.Input[str] expiration_date_utc: Expiration date of the rule, if value is not provided or provided as null this field will default to the maximum allowed expiration date.
        :param pulumi.Input[str] reason: The reason for dismissing the alert
        :param pulumi.Input[Union[str, 'RuleState']] state: Possible states of the rule
        :param pulumi.Input[pulumi.InputType['SuppressionAlertsScopeArgs']] suppression_alerts_scope: The suppression conditions
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            if alert_type is None and not opts.urn:
                raise TypeError("Missing required property 'alert_type'")
            __props__['alert_type'] = alert_type
            if alerts_suppression_rule_name is None and not opts.urn:
                raise TypeError("Missing required property 'alerts_suppression_rule_name'")
            __props__['alerts_suppression_rule_name'] = alerts_suppression_rule_name
            __props__['comment'] = comment
            __props__['expiration_date_utc'] = expiration_date_utc
            if reason is None and not opts.urn:
                raise TypeError("Missing required property 'reason'")
            __props__['reason'] = reason
            if state is None and not opts.urn:
                raise TypeError("Missing required property 'state'")
            __props__['state'] = state
            __props__['suppression_alerts_scope'] = suppression_alerts_scope
            __props__['last_modified_utc'] = None
            __props__['name'] = None
            __props__['type'] = None
        super(AlertsSuppressionRule, __self__).__init__(
            'azure-nextgen:security/v20190101preview:AlertsSuppressionRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AlertsSuppressionRule':
        """
        Get an existing AlertsSuppressionRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return AlertsSuppressionRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="alertType")
    def alert_type(self) -> pulumi.Output[str]:
        """
        Type of the alert to automatically suppress. For all alert types, use '*'
        """
        return pulumi.get(self, "alert_type")

    @property
    @pulumi.getter
    def comment(self) -> pulumi.Output[Optional[str]]:
        """
        Any comment regarding the rule
        """
        return pulumi.get(self, "comment")

    @property
    @pulumi.getter(name="expirationDateUtc")
    def expiration_date_utc(self) -> pulumi.Output[Optional[str]]:
        """
        Expiration date of the rule, if value is not provided or provided as null this field will default to the maximum allowed expiration date.
        """
        return pulumi.get(self, "expiration_date_utc")

    @property
    @pulumi.getter(name="lastModifiedUtc")
    def last_modified_utc(self) -> pulumi.Output[str]:
        """
        The last time this rule was modified
        """
        return pulumi.get(self, "last_modified_utc")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def reason(self) -> pulumi.Output[str]:
        """
        The reason for dismissing the alert
        """
        return pulumi.get(self, "reason")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        Possible states of the rule
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="suppressionAlertsScope")
    def suppression_alerts_scope(self) -> pulumi.Output[Optional['outputs.SuppressionAlertsScopeResponse']]:
        """
        The suppression conditions
        """
        return pulumi.get(self, "suppression_alerts_scope")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

