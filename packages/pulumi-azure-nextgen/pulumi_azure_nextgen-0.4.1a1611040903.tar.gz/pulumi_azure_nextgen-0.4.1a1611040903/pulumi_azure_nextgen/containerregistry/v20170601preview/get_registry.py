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
    'GetRegistryResult',
    'AwaitableGetRegistryResult',
    'get_registry',
]

@pulumi.output_type
class GetRegistryResult:
    """
    An object that represents a container registry.
    """
    def __init__(__self__, admin_user_enabled=None, creation_date=None, id=None, location=None, login_server=None, name=None, provisioning_state=None, sku=None, status=None, storage_account=None, tags=None, type=None):
        if admin_user_enabled and not isinstance(admin_user_enabled, bool):
            raise TypeError("Expected argument 'admin_user_enabled' to be a bool")
        pulumi.set(__self__, "admin_user_enabled", admin_user_enabled)
        if creation_date and not isinstance(creation_date, str):
            raise TypeError("Expected argument 'creation_date' to be a str")
        pulumi.set(__self__, "creation_date", creation_date)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if login_server and not isinstance(login_server, str):
            raise TypeError("Expected argument 'login_server' to be a str")
        pulumi.set(__self__, "login_server", login_server)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if status and not isinstance(status, dict):
            raise TypeError("Expected argument 'status' to be a dict")
        pulumi.set(__self__, "status", status)
        if storage_account and not isinstance(storage_account, dict):
            raise TypeError("Expected argument 'storage_account' to be a dict")
        pulumi.set(__self__, "storage_account", storage_account)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="adminUserEnabled")
    def admin_user_enabled(self) -> Optional[bool]:
        """
        The value that indicates whether the admin user is enabled.
        """
        return pulumi.get(self, "admin_user_enabled")

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> str:
        """
        The creation date of the container registry in ISO8601 format.
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The location of the resource. This cannot be changed after the resource is created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="loginServer")
    def login_server(self) -> str:
        """
        The URL that can be used to log into the container registry.
        """
        return pulumi.get(self, "login_server")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the container registry at the time the operation was called.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def sku(self) -> 'outputs.SkuResponse':
        """
        The SKU of the container registry.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def status(self) -> 'outputs.StatusResponse':
        """
        The status of the container registry at the time the operation was called.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="storageAccount")
    def storage_account(self) -> Optional['outputs.StorageAccountPropertiesResponse']:
        """
        The properties of the storage account for the container registry. Only applicable to Basic SKU.
        """
        return pulumi.get(self, "storage_account")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The tags of the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetRegistryResult(GetRegistryResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRegistryResult(
            admin_user_enabled=self.admin_user_enabled,
            creation_date=self.creation_date,
            id=self.id,
            location=self.location,
            login_server=self.login_server,
            name=self.name,
            provisioning_state=self.provisioning_state,
            sku=self.sku,
            status=self.status,
            storage_account=self.storage_account,
            tags=self.tags,
            type=self.type)


def get_registry(registry_name: Optional[str] = None,
                 resource_group_name: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRegistryResult:
    """
    Use this data source to access information about an existing resource.

    :param str registry_name: The name of the container registry.
    :param str resource_group_name: The name of the resource group to which the container registry belongs.
    """
    __args__ = dict()
    __args__['registryName'] = registry_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:containerregistry/v20170601preview:getRegistry', __args__, opts=opts, typ=GetRegistryResult).value

    return AwaitableGetRegistryResult(
        admin_user_enabled=__ret__.admin_user_enabled,
        creation_date=__ret__.creation_date,
        id=__ret__.id,
        location=__ret__.location,
        login_server=__ret__.login_server,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        sku=__ret__.sku,
        status=__ret__.status,
        storage_account=__ret__.storage_account,
        tags=__ret__.tags,
        type=__ret__.type)
