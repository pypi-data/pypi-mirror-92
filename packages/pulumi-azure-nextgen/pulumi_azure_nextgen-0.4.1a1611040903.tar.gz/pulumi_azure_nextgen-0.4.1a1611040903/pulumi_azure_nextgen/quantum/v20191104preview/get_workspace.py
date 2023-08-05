# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs

__all__ = [
    'GetWorkspaceResult',
    'AwaitableGetWorkspaceResult',
    'get_workspace',
]

@pulumi.output_type
class GetWorkspaceResult:
    """
    The resource proxy definition object for quantum workspace.
    """
    def __init__(__self__, id=None, identity=None, location=None, name=None, providers=None, provisioning_state=None, storage_account=None, tags=None, type=None, usable=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if providers and not isinstance(providers, list):
            raise TypeError("Expected argument 'providers' to be a list")
        pulumi.set(__self__, "providers", providers)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if storage_account and not isinstance(storage_account, str):
            raise TypeError("Expected argument 'storage_account' to be a str")
        pulumi.set(__self__, "storage_account", storage_account)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if usable and not isinstance(usable, str):
            raise TypeError("Expected argument 'usable' to be a str")
        pulumi.set(__self__, "usable", usable)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.QuantumWorkspaceResponseIdentity']:
        """
        Managed Identity information.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def providers(self) -> Optional[Sequence['outputs.ProviderResponse']]:
        """
        List of Providers selected for this Workspace
        """
        return pulumi.get(self, "providers")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning status field
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="storageAccount")
    def storage_account(self) -> Optional[str]:
        """
        ARM Resource Id of the storage account associated with this workspace.
        """
        return pulumi.get(self, "storage_account")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def usable(self) -> str:
        """
        Whether the current workspace is ready to accept Jobs.
        """
        return pulumi.get(self, "usable")


class AwaitableGetWorkspaceResult(GetWorkspaceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWorkspaceResult(
            id=self.id,
            identity=self.identity,
            location=self.location,
            name=self.name,
            providers=self.providers,
            provisioning_state=self.provisioning_state,
            storage_account=self.storage_account,
            tags=self.tags,
            type=self.type,
            usable=self.usable)


def get_workspace(resource_group_name: Optional[str] = None,
                  workspace_name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWorkspaceResult:
    """
    Use this data source to access information about an existing resource.

    :param str resource_group_name: The name of the resource group.
    :param str workspace_name: The name of the quantum workspace resource.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['workspaceName'] = workspace_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:quantum/v20191104preview:getWorkspace', __args__, opts=opts, typ=GetWorkspaceResult).value

    return AwaitableGetWorkspaceResult(
        id=__ret__.id,
        identity=__ret__.identity,
        location=__ret__.location,
        name=__ret__.name,
        providers=__ret__.providers,
        provisioning_state=__ret__.provisioning_state,
        storage_account=__ret__.storage_account,
        tags=__ret__.tags,
        type=__ret__.type,
        usable=__ret__.usable)
