# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'GetArtifactResult',
    'AwaitableGetArtifactResult',
    'get_artifact',
]

@pulumi.output_type
class GetArtifactResult:
    """
    Represents a blueprint artifact.
    """
    def __init__(__self__, id=None, kind=None, name=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        String Id used to locate any resource on Azure.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Specifies the kind of blueprint artifact.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of this resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of this resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetArtifactResult(GetArtifactResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetArtifactResult(
            id=self.id,
            kind=self.kind,
            name=self.name,
            type=self.type)


def get_artifact(artifact_name: Optional[str] = None,
                 blueprint_name: Optional[str] = None,
                 resource_scope: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetArtifactResult:
    """
    Use this data source to access information about an existing resource.

    :param str artifact_name: Name of the blueprint artifact.
    :param str blueprint_name: Name of the blueprint definition.
    :param str resource_scope: The scope of the resource. Valid scopes are: management group (format: '/providers/Microsoft.Management/managementGroups/{managementGroup}'), subscription (format: '/subscriptions/{subscriptionId}').
    """
    __args__ = dict()
    __args__['artifactName'] = artifact_name
    __args__['blueprintName'] = blueprint_name
    __args__['resourceScope'] = resource_scope
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:blueprint/v20181101preview:getArtifact', __args__, opts=opts, typ=GetArtifactResult).value

    return AwaitableGetArtifactResult(
        id=__ret__.id,
        kind=__ret__.kind,
        name=__ret__.name,
        type=__ret__.type)
