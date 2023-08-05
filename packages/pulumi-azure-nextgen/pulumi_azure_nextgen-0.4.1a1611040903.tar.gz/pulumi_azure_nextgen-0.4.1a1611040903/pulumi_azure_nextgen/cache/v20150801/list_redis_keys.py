# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'ListRedisKeysResult',
    'AwaitableListRedisKeysResult',
    'list_redis_keys',
]

@pulumi.output_type
class ListRedisKeysResult:
    """
    The response of Redis list keys operation.
    """
    def __init__(__self__, primary_key=None, secondary_key=None):
        if primary_key and not isinstance(primary_key, str):
            raise TypeError("Expected argument 'primary_key' to be a str")
        pulumi.set(__self__, "primary_key", primary_key)
        if secondary_key and not isinstance(secondary_key, str):
            raise TypeError("Expected argument 'secondary_key' to be a str")
        pulumi.set(__self__, "secondary_key", secondary_key)

    @property
    @pulumi.getter(name="primaryKey")
    def primary_key(self) -> Optional[str]:
        """
        The current primary key that clients can use to authenticate with Redis cache.
        """
        return pulumi.get(self, "primary_key")

    @property
    @pulumi.getter(name="secondaryKey")
    def secondary_key(self) -> Optional[str]:
        """
        The current secondary key that clients can use to authenticate with Redis cache.
        """
        return pulumi.get(self, "secondary_key")


class AwaitableListRedisKeysResult(ListRedisKeysResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListRedisKeysResult(
            primary_key=self.primary_key,
            secondary_key=self.secondary_key)


def list_redis_keys(name: Optional[str] = None,
                    resource_group_name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListRedisKeysResult:
    """
    Use this data source to access information about an existing resource.

    :param str name: The name of the Redis cache.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:cache/v20150801:listRedisKeys', __args__, opts=opts, typ=ListRedisKeysResult).value

    return AwaitableListRedisKeysResult(
        primary_key=__ret__.primary_key,
        secondary_key=__ret__.secondary_key)
