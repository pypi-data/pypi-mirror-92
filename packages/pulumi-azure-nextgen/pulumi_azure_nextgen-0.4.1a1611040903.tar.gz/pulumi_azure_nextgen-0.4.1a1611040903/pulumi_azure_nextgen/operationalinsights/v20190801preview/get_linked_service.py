# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'GetLinkedServiceResult',
    'AwaitableGetLinkedServiceResult',
    'get_linked_service',
]

@pulumi.output_type
class GetLinkedServiceResult:
    """
    The top level Linked service resource container.
    """
    def __init__(__self__, id=None, name=None, resource_id=None, type=None, write_access_resource_id=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource_id and not isinstance(resource_id, str):
            raise TypeError("Expected argument 'resource_id' to be a str")
        pulumi.set(__self__, "resource_id", resource_id)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if write_access_resource_id and not isinstance(write_access_resource_id, str):
            raise TypeError("Expected argument 'write_access_resource_id' to be a str")
        pulumi.set(__self__, "write_access_resource_id", write_access_resource_id)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[str]:
        """
        The resource id of the resource that will be linked to the workspace. This should be used for linking resources which require read access
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="writeAccessResourceId")
    def write_access_resource_id(self) -> Optional[str]:
        """
        The resource id of the resource that will be linked to the workspace. This should be used for linking resources which require write access
        """
        return pulumi.get(self, "write_access_resource_id")


class AwaitableGetLinkedServiceResult(GetLinkedServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLinkedServiceResult(
            id=self.id,
            name=self.name,
            resource_id=self.resource_id,
            type=self.type,
            write_access_resource_id=self.write_access_resource_id)


def get_linked_service(linked_service_name: Optional[str] = None,
                       resource_group_name: Optional[str] = None,
                       workspace_name: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLinkedServiceResult:
    """
    Use this data source to access information about an existing resource.

    :param str linked_service_name: Name of the linked service.
    :param str resource_group_name: The name of the resource group to get. The name is case insensitive.
    :param str workspace_name: Name of the Log Analytics Workspace that contains the linkedServices resource
    """
    __args__ = dict()
    __args__['linkedServiceName'] = linked_service_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:operationalinsights/v20190801preview:getLinkedService', __args__, opts=opts, typ=GetLinkedServiceResult).value

    return AwaitableGetLinkedServiceResult(
        id=__ret__.id,
        name=__ret__.name,
        resource_id=__ret__.resource_id,
        type=__ret__.type,
        write_access_resource_id=__ret__.write_access_resource_id)
