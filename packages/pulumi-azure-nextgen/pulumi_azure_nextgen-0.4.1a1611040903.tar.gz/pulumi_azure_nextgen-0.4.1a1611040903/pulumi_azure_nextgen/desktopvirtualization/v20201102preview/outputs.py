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
    'MsixPackageApplicationsResponse',
    'MsixPackageDependenciesResponse',
    'RegistrationInfoResponse',
]

@pulumi.output_type
class MsixPackageApplicationsResponse(dict):
    """
    Schema for MSIX Package Application properties.
    """
    def __init__(__self__, *,
                 app_id: Optional[str] = None,
                 app_user_model_id: Optional[str] = None,
                 description: Optional[str] = None,
                 friendly_name: Optional[str] = None,
                 icon_image_name: Optional[str] = None,
                 raw_icon: Optional[str] = None,
                 raw_png: Optional[str] = None):
        """
        Schema for MSIX Package Application properties.
        :param str app_id: Package Application Id, found in appxmanifest.xml.
        :param str app_user_model_id: Used to activate Package Application. Consists of Package Name and ApplicationID. Found in appxmanifest.xml.
        :param str description: Description of Package Application.
        :param str friendly_name: User friendly name.
        :param str icon_image_name: User friendly name.
        :param str raw_icon: the icon a 64 bit string as a byte array.
        :param str raw_png: the icon a 64 bit string as a byte array.
        """
        if app_id is not None:
            pulumi.set(__self__, "app_id", app_id)
        if app_user_model_id is not None:
            pulumi.set(__self__, "app_user_model_id", app_user_model_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if friendly_name is not None:
            pulumi.set(__self__, "friendly_name", friendly_name)
        if icon_image_name is not None:
            pulumi.set(__self__, "icon_image_name", icon_image_name)
        if raw_icon is not None:
            pulumi.set(__self__, "raw_icon", raw_icon)
        if raw_png is not None:
            pulumi.set(__self__, "raw_png", raw_png)

    @property
    @pulumi.getter(name="appId")
    def app_id(self) -> Optional[str]:
        """
        Package Application Id, found in appxmanifest.xml.
        """
        return pulumi.get(self, "app_id")

    @property
    @pulumi.getter(name="appUserModelID")
    def app_user_model_id(self) -> Optional[str]:
        """
        Used to activate Package Application. Consists of Package Name and ApplicationID. Found in appxmanifest.xml.
        """
        return pulumi.get(self, "app_user_model_id")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description of Package Application.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> Optional[str]:
        """
        User friendly name.
        """
        return pulumi.get(self, "friendly_name")

    @property
    @pulumi.getter(name="iconImageName")
    def icon_image_name(self) -> Optional[str]:
        """
        User friendly name.
        """
        return pulumi.get(self, "icon_image_name")

    @property
    @pulumi.getter(name="rawIcon")
    def raw_icon(self) -> Optional[str]:
        """
        the icon a 64 bit string as a byte array.
        """
        return pulumi.get(self, "raw_icon")

    @property
    @pulumi.getter(name="rawPng")
    def raw_png(self) -> Optional[str]:
        """
        the icon a 64 bit string as a byte array.
        """
        return pulumi.get(self, "raw_png")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class MsixPackageDependenciesResponse(dict):
    """
    Schema for MSIX Package Dependencies properties.
    """
    def __init__(__self__, *,
                 dependency_name: Optional[str] = None,
                 min_version: Optional[str] = None,
                 publisher: Optional[str] = None):
        """
        Schema for MSIX Package Dependencies properties.
        :param str dependency_name: Name of package dependency.
        :param str min_version: Dependency version required.
        :param str publisher: Name of dependency publisher.
        """
        if dependency_name is not None:
            pulumi.set(__self__, "dependency_name", dependency_name)
        if min_version is not None:
            pulumi.set(__self__, "min_version", min_version)
        if publisher is not None:
            pulumi.set(__self__, "publisher", publisher)

    @property
    @pulumi.getter(name="dependencyName")
    def dependency_name(self) -> Optional[str]:
        """
        Name of package dependency.
        """
        return pulumi.get(self, "dependency_name")

    @property
    @pulumi.getter(name="minVersion")
    def min_version(self) -> Optional[str]:
        """
        Dependency version required.
        """
        return pulumi.get(self, "min_version")

    @property
    @pulumi.getter
    def publisher(self) -> Optional[str]:
        """
        Name of dependency publisher.
        """
        return pulumi.get(self, "publisher")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class RegistrationInfoResponse(dict):
    """
    Represents a RegistrationInfo definition.
    """
    def __init__(__self__, *,
                 expiration_time: Optional[str] = None,
                 registration_token_operation: Optional[str] = None,
                 token: Optional[str] = None):
        """
        Represents a RegistrationInfo definition.
        :param str expiration_time: Expiration time of registration token.
        :param str registration_token_operation: The type of resetting the token.
        :param str token: The registration token base64 encoded string.
        """
        if expiration_time is not None:
            pulumi.set(__self__, "expiration_time", expiration_time)
        if registration_token_operation is not None:
            pulumi.set(__self__, "registration_token_operation", registration_token_operation)
        if token is not None:
            pulumi.set(__self__, "token", token)

    @property
    @pulumi.getter(name="expirationTime")
    def expiration_time(self) -> Optional[str]:
        """
        Expiration time of registration token.
        """
        return pulumi.get(self, "expiration_time")

    @property
    @pulumi.getter(name="registrationTokenOperation")
    def registration_token_operation(self) -> Optional[str]:
        """
        The type of resetting the token.
        """
        return pulumi.get(self, "registration_token_operation")

    @property
    @pulumi.getter
    def token(self) -> Optional[str]:
        """
        The registration token base64 encoded string.
        """
        return pulumi.get(self, "token")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


