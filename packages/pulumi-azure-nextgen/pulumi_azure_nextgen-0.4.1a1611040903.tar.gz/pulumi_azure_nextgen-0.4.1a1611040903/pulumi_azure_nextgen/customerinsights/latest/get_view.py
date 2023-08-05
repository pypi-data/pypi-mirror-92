# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'GetViewResult',
    'AwaitableGetViewResult',
    'get_view',
]

@pulumi.output_type
class GetViewResult:
    """
    The view resource format.
    """
    def __init__(__self__, changed=None, created=None, definition=None, display_name=None, id=None, name=None, tenant_id=None, type=None, user_id=None, view_name=None):
        if changed and not isinstance(changed, str):
            raise TypeError("Expected argument 'changed' to be a str")
        pulumi.set(__self__, "changed", changed)
        if created and not isinstance(created, str):
            raise TypeError("Expected argument 'created' to be a str")
        pulumi.set(__self__, "created", created)
        if definition and not isinstance(definition, str):
            raise TypeError("Expected argument 'definition' to be a str")
        pulumi.set(__self__, "definition", definition)
        if display_name and not isinstance(display_name, dict):
            raise TypeError("Expected argument 'display_name' to be a dict")
        pulumi.set(__self__, "display_name", display_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tenant_id and not isinstance(tenant_id, str):
            raise TypeError("Expected argument 'tenant_id' to be a str")
        pulumi.set(__self__, "tenant_id", tenant_id)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if user_id and not isinstance(user_id, str):
            raise TypeError("Expected argument 'user_id' to be a str")
        pulumi.set(__self__, "user_id", user_id)
        if view_name and not isinstance(view_name, str):
            raise TypeError("Expected argument 'view_name' to be a str")
        pulumi.set(__self__, "view_name", view_name)

    @property
    @pulumi.getter
    def changed(self) -> str:
        """
        Date time when view was last modified.
        """
        return pulumi.get(self, "changed")

    @property
    @pulumi.getter
    def created(self) -> str:
        """
        Date time when view was created.
        """
        return pulumi.get(self, "created")

    @property
    @pulumi.getter
    def definition(self) -> str:
        """
        View definition.
        """
        return pulumi.get(self, "definition")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[Mapping[str, str]]:
        """
        Localized display name for the view.
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
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        the hub name.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> Optional[str]:
        """
        the user ID.
        """
        return pulumi.get(self, "user_id")

    @property
    @pulumi.getter(name="viewName")
    def view_name(self) -> str:
        """
        Name of the view.
        """
        return pulumi.get(self, "view_name")


class AwaitableGetViewResult(GetViewResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetViewResult(
            changed=self.changed,
            created=self.created,
            definition=self.definition,
            display_name=self.display_name,
            id=self.id,
            name=self.name,
            tenant_id=self.tenant_id,
            type=self.type,
            user_id=self.user_id,
            view_name=self.view_name)


def get_view(hub_name: Optional[str] = None,
             resource_group_name: Optional[str] = None,
             user_id: Optional[str] = None,
             view_name: Optional[str] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetViewResult:
    """
    Use this data source to access information about an existing resource.

    :param str hub_name: The name of the hub.
    :param str resource_group_name: The name of the resource group.
    :param str user_id: The user ID. Use * to retrieve hub level view.
    :param str view_name: The name of the view.
    """
    __args__ = dict()
    __args__['hubName'] = hub_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['userId'] = user_id
    __args__['viewName'] = view_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:customerinsights/latest:getView', __args__, opts=opts, typ=GetViewResult).value

    return AwaitableGetViewResult(
        changed=__ret__.changed,
        created=__ret__.created,
        definition=__ret__.definition,
        display_name=__ret__.display_name,
        id=__ret__.id,
        name=__ret__.name,
        tenant_id=__ret__.tenant_id,
        type=__ret__.type,
        user_id=__ret__.user_id,
        view_name=__ret__.view_name)
