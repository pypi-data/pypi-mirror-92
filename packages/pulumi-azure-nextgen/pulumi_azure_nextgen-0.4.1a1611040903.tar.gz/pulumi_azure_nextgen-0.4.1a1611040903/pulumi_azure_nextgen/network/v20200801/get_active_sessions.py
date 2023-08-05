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
    'GetActiveSessionsResult',
    'AwaitableGetActiveSessionsResult',
    'get_active_sessions',
]

@pulumi.output_type
class GetActiveSessionsResult:
    """
    Response for GetActiveSessions.
    """
    def __init__(__self__, next_link=None, value=None):
        if next_link and not isinstance(next_link, str):
            raise TypeError("Expected argument 'next_link' to be a str")
        pulumi.set(__self__, "next_link", next_link)
        if value and not isinstance(value, list):
            raise TypeError("Expected argument 'value' to be a list")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="nextLink")
    def next_link(self) -> Optional[str]:
        """
        The URL to get the next set of results.
        """
        return pulumi.get(self, "next_link")

    @property
    @pulumi.getter
    def value(self) -> Optional[Sequence['outputs.BastionActiveSessionResponseResult']]:
        """
        List of active sessions on the bastion.
        """
        return pulumi.get(self, "value")


class AwaitableGetActiveSessionsResult(GetActiveSessionsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetActiveSessionsResult(
            next_link=self.next_link,
            value=self.value)


def get_active_sessions(bastion_host_name: Optional[str] = None,
                        resource_group_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetActiveSessionsResult:
    """
    Use this data source to access information about an existing resource.

    :param str bastion_host_name: The name of the Bastion Host.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['bastionHostName'] = bastion_host_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:network/v20200801:getActiveSessions', __args__, opts=opts, typ=GetActiveSessionsResult).value

    return AwaitableGetActiveSessionsResult(
        next_link=__ret__.next_link,
        value=__ret__.value)
