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
    'BlueprintStatusResponse',
    'ParameterDefinitionResponse',
    'ResourceGroupDefinitionResponse',
]

@pulumi.output_type
class BlueprintStatusResponse(dict):
    """
    The status of the blueprint. This field is readonly.
    """
    def __init__(__self__, *,
                 last_modified: str,
                 time_created: str):
        """
        The status of the blueprint. This field is readonly.
        :param str last_modified: Last modified time of this blueprint.
        :param str time_created: Creation time of this blueprint.
        """
        pulumi.set(__self__, "last_modified", last_modified)
        pulumi.set(__self__, "time_created", time_created)

    @property
    @pulumi.getter(name="lastModified")
    def last_modified(self) -> str:
        """
        Last modified time of this blueprint.
        """
        return pulumi.get(self, "last_modified")

    @property
    @pulumi.getter(name="timeCreated")
    def time_created(self) -> str:
        """
        Creation time of this blueprint.
        """
        return pulumi.get(self, "time_created")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ParameterDefinitionResponse(dict):
    """
    Represent a parameter with constrains and metadata.
    """
    def __init__(__self__, *,
                 type: str,
                 allowed_values: Optional[Sequence[Any]] = None,
                 default_value: Optional[Any] = None,
                 description: Optional[str] = None,
                 display_name: Optional[str] = None,
                 strong_type: Optional[str] = None):
        """
        Represent a parameter with constrains and metadata.
        :param str type: Allowed data types for Azure Resource Manager template parameters.
        :param Sequence[Any] allowed_values: Array of allowed values for this parameter.
        :param Any default_value: Default Value for this parameter.
        :param str description: Description of this parameter/resourceGroup.
        :param str display_name: DisplayName of this parameter/resourceGroup.
        :param str strong_type: StrongType for UI to render rich experience during assignment time.
        """
        pulumi.set(__self__, "type", type)
        if allowed_values is not None:
            pulumi.set(__self__, "allowed_values", allowed_values)
        if default_value is not None:
            pulumi.set(__self__, "default_value", default_value)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if strong_type is not None:
            pulumi.set(__self__, "strong_type", strong_type)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Allowed data types for Azure Resource Manager template parameters.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="allowedValues")
    def allowed_values(self) -> Optional[Sequence[Any]]:
        """
        Array of allowed values for this parameter.
        """
        return pulumi.get(self, "allowed_values")

    @property
    @pulumi.getter(name="defaultValue")
    def default_value(self) -> Optional[Any]:
        """
        Default Value for this parameter.
        """
        return pulumi.get(self, "default_value")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description of this parameter/resourceGroup.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        DisplayName of this parameter/resourceGroup.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="strongType")
    def strong_type(self) -> Optional[str]:
        """
        StrongType for UI to render rich experience during assignment time.
        """
        return pulumi.get(self, "strong_type")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ResourceGroupDefinitionResponse(dict):
    """
    Represents an Azure resource group in a Blueprint definition.
    """
    def __init__(__self__, *,
                 depends_on: Optional[Sequence[str]] = None,
                 description: Optional[str] = None,
                 display_name: Optional[str] = None,
                 location: Optional[str] = None,
                 name: Optional[str] = None,
                 strong_type: Optional[str] = None):
        """
        Represents an Azure resource group in a Blueprint definition.
        :param Sequence[str] depends_on: Artifacts which need to be deployed before this resource group.
        :param str description: Description of this parameter/resourceGroup.
        :param str display_name: DisplayName of this parameter/resourceGroup.
        :param str location: Location of this resourceGroup, leave empty if the resource group location will be specified during the Blueprint assignment.
        :param str name: Name of this resourceGroup, leave empty if the resource group name will be specified during the Blueprint assignment.
        :param str strong_type: StrongType for UI to render rich experience during assignment time.
        """
        if depends_on is not None:
            pulumi.set(__self__, "depends_on", depends_on)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if strong_type is not None:
            pulumi.set(__self__, "strong_type", strong_type)

    @property
    @pulumi.getter(name="dependsOn")
    def depends_on(self) -> Optional[Sequence[str]]:
        """
        Artifacts which need to be deployed before this resource group.
        """
        return pulumi.get(self, "depends_on")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description of this parameter/resourceGroup.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        DisplayName of this parameter/resourceGroup.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Location of this resourceGroup, leave empty if the resource group location will be specified during the Blueprint assignment.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Name of this resourceGroup, leave empty if the resource group name will be specified during the Blueprint assignment.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="strongType")
    def strong_type(self) -> Optional[str]:
        """
        StrongType for UI to render rich experience during assignment time.
        """
        return pulumi.get(self, "strong_type")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


