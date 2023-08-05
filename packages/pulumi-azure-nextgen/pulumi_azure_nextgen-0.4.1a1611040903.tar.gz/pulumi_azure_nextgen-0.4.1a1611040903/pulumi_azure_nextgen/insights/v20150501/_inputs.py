# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from ._enums import *

__all__ = [
    'ApplicationInsightsComponentAnalyticsItemPropertiesArgs',
    'ApplicationInsightsComponentDataVolumeCapArgs',
    'WebTestGeolocationArgs',
    'WebTestPropertiesConfigurationArgs',
]

@pulumi.input_type
class ApplicationInsightsComponentAnalyticsItemPropertiesArgs:
    def __init__(__self__, *,
                 function_alias: Optional[pulumi.Input[str]] = None):
        """
        A set of properties that can be defined in the context of a specific item type. Each type may have its own properties.
        :param pulumi.Input[str] function_alias: A function alias, used when the type of the item is Function
        """
        if function_alias is not None:
            pulumi.set(__self__, "function_alias", function_alias)

    @property
    @pulumi.getter(name="functionAlias")
    def function_alias(self) -> Optional[pulumi.Input[str]]:
        """
        A function alias, used when the type of the item is Function
        """
        return pulumi.get(self, "function_alias")

    @function_alias.setter
    def function_alias(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "function_alias", value)


@pulumi.input_type
class ApplicationInsightsComponentDataVolumeCapArgs:
    def __init__(__self__, *,
                 cap: Optional[pulumi.Input[float]] = None,
                 stop_send_notification_when_hit_cap: Optional[pulumi.Input[bool]] = None,
                 stop_send_notification_when_hit_threshold: Optional[pulumi.Input[bool]] = None,
                 warning_threshold: Optional[pulumi.Input[int]] = None):
        """
        An Application Insights component daily data volume cap
        :param pulumi.Input[float] cap: Daily data volume cap in GB.
        :param pulumi.Input[bool] stop_send_notification_when_hit_cap: Do not send a notification email when the daily data volume cap is met.
        :param pulumi.Input[bool] stop_send_notification_when_hit_threshold: Reserved, not used for now.
        :param pulumi.Input[int] warning_threshold: Reserved, not used for now.
        """
        if cap is not None:
            pulumi.set(__self__, "cap", cap)
        if stop_send_notification_when_hit_cap is not None:
            pulumi.set(__self__, "stop_send_notification_when_hit_cap", stop_send_notification_when_hit_cap)
        if stop_send_notification_when_hit_threshold is not None:
            pulumi.set(__self__, "stop_send_notification_when_hit_threshold", stop_send_notification_when_hit_threshold)
        if warning_threshold is not None:
            pulumi.set(__self__, "warning_threshold", warning_threshold)

    @property
    @pulumi.getter
    def cap(self) -> Optional[pulumi.Input[float]]:
        """
        Daily data volume cap in GB.
        """
        return pulumi.get(self, "cap")

    @cap.setter
    def cap(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "cap", value)

    @property
    @pulumi.getter(name="stopSendNotificationWhenHitCap")
    def stop_send_notification_when_hit_cap(self) -> Optional[pulumi.Input[bool]]:
        """
        Do not send a notification email when the daily data volume cap is met.
        """
        return pulumi.get(self, "stop_send_notification_when_hit_cap")

    @stop_send_notification_when_hit_cap.setter
    def stop_send_notification_when_hit_cap(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "stop_send_notification_when_hit_cap", value)

    @property
    @pulumi.getter(name="stopSendNotificationWhenHitThreshold")
    def stop_send_notification_when_hit_threshold(self) -> Optional[pulumi.Input[bool]]:
        """
        Reserved, not used for now.
        """
        return pulumi.get(self, "stop_send_notification_when_hit_threshold")

    @stop_send_notification_when_hit_threshold.setter
    def stop_send_notification_when_hit_threshold(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "stop_send_notification_when_hit_threshold", value)

    @property
    @pulumi.getter(name="warningThreshold")
    def warning_threshold(self) -> Optional[pulumi.Input[int]]:
        """
        Reserved, not used for now.
        """
        return pulumi.get(self, "warning_threshold")

    @warning_threshold.setter
    def warning_threshold(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "warning_threshold", value)


@pulumi.input_type
class WebTestGeolocationArgs:
    def __init__(__self__, *,
                 location: Optional[pulumi.Input[str]] = None):
        """
        Geo-physical location to run a web test from. You must specify one or more locations for the test to run from.
        :param pulumi.Input[str] location: Location ID for the webtest to run from.
        """
        if location is not None:
            pulumi.set(__self__, "location", location)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Location ID for the webtest to run from.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)


@pulumi.input_type
class WebTestPropertiesConfigurationArgs:
    def __init__(__self__, *,
                 web_test: Optional[pulumi.Input[str]] = None):
        """
        An XML configuration specification for a WebTest.
        :param pulumi.Input[str] web_test: The XML specification of a WebTest to run against an application.
        """
        if web_test is not None:
            pulumi.set(__self__, "web_test", web_test)

    @property
    @pulumi.getter(name="webTest")
    def web_test(self) -> Optional[pulumi.Input[str]]:
        """
        The XML specification of a WebTest to run against an application.
        """
        return pulumi.get(self, "web_test")

    @web_test.setter
    def web_test(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "web_test", value)


