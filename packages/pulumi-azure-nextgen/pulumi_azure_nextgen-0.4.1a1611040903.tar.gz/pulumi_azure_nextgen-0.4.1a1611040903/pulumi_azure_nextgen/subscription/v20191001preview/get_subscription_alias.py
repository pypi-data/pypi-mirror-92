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
    'GetSubscriptionAliasResult',
    'AwaitableGetSubscriptionAliasResult',
    'get_subscription_alias',
]

@pulumi.output_type
class GetSubscriptionAliasResult:
    """
    Subscription Information with the alias.
    """
    def __init__(__self__, id=None, name=None, properties=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified ID for the alias resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Alias ID.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.PutAliasResponsePropertiesResponse':
        """
        Put Alias response properties.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type, Microsoft.Subscription/aliases.
        """
        return pulumi.get(self, "type")


class AwaitableGetSubscriptionAliasResult(GetSubscriptionAliasResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSubscriptionAliasResult(
            id=self.id,
            name=self.name,
            properties=self.properties,
            type=self.type)


def get_subscription_alias(alias_name: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSubscriptionAliasResult:
    """
    Use this data source to access information about an existing resource.

    :param str alias_name: Alias Name
    """
    __args__ = dict()
    __args__['aliasName'] = alias_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:subscription/v20191001preview:getSubscriptionAlias', __args__, opts=opts, typ=GetSubscriptionAliasResult).value

    return AwaitableGetSubscriptionAliasResult(
        id=__ret__.id,
        name=__ret__.name,
        properties=__ret__.properties,
        type=__ret__.type)
