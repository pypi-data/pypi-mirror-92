# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'GetConnectorResult',
    'AwaitableGetConnectorResult',
    'get_connector',
]

@pulumi.output_type
class GetConnectorResult:
    """
    The connector resource format.
    """
    def __init__(__self__, connector_id=None, connector_name=None, connector_properties=None, connector_type=None, created=None, description=None, display_name=None, id=None, is_internal=None, last_modified=None, name=None, state=None, tenant_id=None, type=None):
        if connector_id and not isinstance(connector_id, int):
            raise TypeError("Expected argument 'connector_id' to be a int")
        pulumi.set(__self__, "connector_id", connector_id)
        if connector_name and not isinstance(connector_name, str):
            raise TypeError("Expected argument 'connector_name' to be a str")
        pulumi.set(__self__, "connector_name", connector_name)
        if connector_properties and not isinstance(connector_properties, dict):
            raise TypeError("Expected argument 'connector_properties' to be a dict")
        pulumi.set(__self__, "connector_properties", connector_properties)
        if connector_type and not isinstance(connector_type, str):
            raise TypeError("Expected argument 'connector_type' to be a str")
        pulumi.set(__self__, "connector_type", connector_type)
        if created and not isinstance(created, str):
            raise TypeError("Expected argument 'created' to be a str")
        pulumi.set(__self__, "created", created)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_internal and not isinstance(is_internal, bool):
            raise TypeError("Expected argument 'is_internal' to be a bool")
        pulumi.set(__self__, "is_internal", is_internal)
        if last_modified and not isinstance(last_modified, str):
            raise TypeError("Expected argument 'last_modified' to be a str")
        pulumi.set(__self__, "last_modified", last_modified)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if tenant_id and not isinstance(tenant_id, str):
            raise TypeError("Expected argument 'tenant_id' to be a str")
        pulumi.set(__self__, "tenant_id", tenant_id)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="connectorId")
    def connector_id(self) -> int:
        """
        ID of the connector.
        """
        return pulumi.get(self, "connector_id")

    @property
    @pulumi.getter(name="connectorName")
    def connector_name(self) -> Optional[str]:
        """
        Name of the connector.
        """
        return pulumi.get(self, "connector_name")

    @property
    @pulumi.getter(name="connectorProperties")
    def connector_properties(self) -> Mapping[str, Any]:
        """
        The connector properties.
        """
        return pulumi.get(self, "connector_properties")

    @property
    @pulumi.getter(name="connectorType")
    def connector_type(self) -> str:
        """
        Type of connector.
        """
        return pulumi.get(self, "connector_type")

    @property
    @pulumi.getter
    def created(self) -> str:
        """
        The created time.
        """
        return pulumi.get(self, "created")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description of the connector.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        Display name of the connector.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isInternal")
    def is_internal(self) -> Optional[bool]:
        """
        If this is an internal connector.
        """
        return pulumi.get(self, "is_internal")

    @property
    @pulumi.getter(name="lastModified")
    def last_modified(self) -> str:
        """
        The last modified time.
        """
        return pulumi.get(self, "last_modified")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        State of connector.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The hub name.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetConnectorResult(GetConnectorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConnectorResult(
            connector_id=self.connector_id,
            connector_name=self.connector_name,
            connector_properties=self.connector_properties,
            connector_type=self.connector_type,
            created=self.created,
            description=self.description,
            display_name=self.display_name,
            id=self.id,
            is_internal=self.is_internal,
            last_modified=self.last_modified,
            name=self.name,
            state=self.state,
            tenant_id=self.tenant_id,
            type=self.type)


def get_connector(connector_name: Optional[str] = None,
                  hub_name: Optional[str] = None,
                  resource_group_name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConnectorResult:
    """
    Use this data source to access information about an existing resource.

    :param str connector_name: The name of the connector.
    :param str hub_name: The name of the hub.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['connectorName'] = connector_name
    __args__['hubName'] = hub_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:customerinsights/v20170426:getConnector', __args__, opts=opts, typ=GetConnectorResult).value

    return AwaitableGetConnectorResult(
        connector_id=__ret__.connector_id,
        connector_name=__ret__.connector_name,
        connector_properties=__ret__.connector_properties,
        connector_type=__ret__.connector_type,
        created=__ret__.created,
        description=__ret__.description,
        display_name=__ret__.display_name,
        id=__ret__.id,
        is_internal=__ret__.is_internal,
        last_modified=__ret__.last_modified,
        name=__ret__.name,
        state=__ret__.state,
        tenant_id=__ret__.tenant_id,
        type=__ret__.type)
