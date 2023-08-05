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
    'GetAFDOriginResult',
    'AwaitableGetAFDOriginResult',
    'get_afd_origin',
]

@pulumi.output_type
class GetAFDOriginResult:
    """
    CDN origin is the source of the content being delivered via CDN. When the edge nodes represented by an endpoint do not have the requested content cached, they attempt to fetch it from one or more of the configured origins.
    """
    def __init__(__self__, azure_origin=None, deployment_status=None, enabled_state=None, host_name=None, http_port=None, https_port=None, id=None, name=None, origin_host_header=None, priority=None, provisioning_state=None, shared_private_link_resource=None, system_data=None, type=None, weight=None):
        if azure_origin and not isinstance(azure_origin, dict):
            raise TypeError("Expected argument 'azure_origin' to be a dict")
        pulumi.set(__self__, "azure_origin", azure_origin)
        if deployment_status and not isinstance(deployment_status, str):
            raise TypeError("Expected argument 'deployment_status' to be a str")
        pulumi.set(__self__, "deployment_status", deployment_status)
        if enabled_state and not isinstance(enabled_state, str):
            raise TypeError("Expected argument 'enabled_state' to be a str")
        pulumi.set(__self__, "enabled_state", enabled_state)
        if host_name and not isinstance(host_name, str):
            raise TypeError("Expected argument 'host_name' to be a str")
        pulumi.set(__self__, "host_name", host_name)
        if http_port and not isinstance(http_port, int):
            raise TypeError("Expected argument 'http_port' to be a int")
        pulumi.set(__self__, "http_port", http_port)
        if https_port and not isinstance(https_port, int):
            raise TypeError("Expected argument 'https_port' to be a int")
        pulumi.set(__self__, "https_port", https_port)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if origin_host_header and not isinstance(origin_host_header, str):
            raise TypeError("Expected argument 'origin_host_header' to be a str")
        pulumi.set(__self__, "origin_host_header", origin_host_header)
        if priority and not isinstance(priority, int):
            raise TypeError("Expected argument 'priority' to be a int")
        pulumi.set(__self__, "priority", priority)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if shared_private_link_resource and not isinstance(shared_private_link_resource, list):
            raise TypeError("Expected argument 'shared_private_link_resource' to be a list")
        pulumi.set(__self__, "shared_private_link_resource", shared_private_link_resource)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if weight and not isinstance(weight, int):
            raise TypeError("Expected argument 'weight' to be a int")
        pulumi.set(__self__, "weight", weight)

    @property
    @pulumi.getter(name="azureOrigin")
    def azure_origin(self) -> Optional['outputs.ResourceReferenceResponse']:
        """
        Resource reference to the Azure origin resource.
        """
        return pulumi.get(self, "azure_origin")

    @property
    @pulumi.getter(name="deploymentStatus")
    def deployment_status(self) -> str:
        return pulumi.get(self, "deployment_status")

    @property
    @pulumi.getter(name="enabledState")
    def enabled_state(self) -> Optional[str]:
        """
        Whether to enable health probes to be made against backends defined under backendPools. Health probes can only be disabled if there is a single enabled backend in single enabled backend pool.
        """
        return pulumi.get(self, "enabled_state")

    @property
    @pulumi.getter(name="hostName")
    def host_name(self) -> str:
        """
        The address of the origin. Domain names, IPv4 addresses, and IPv6 addresses are supported.This should be unique across all origins in an endpoint.
        """
        return pulumi.get(self, "host_name")

    @property
    @pulumi.getter(name="httpPort")
    def http_port(self) -> Optional[int]:
        """
        The value of the HTTP port. Must be between 1 and 65535.
        """
        return pulumi.get(self, "http_port")

    @property
    @pulumi.getter(name="httpsPort")
    def https_port(self) -> Optional[int]:
        """
        The value of the HTTPS port. Must be between 1 and 65535.
        """
        return pulumi.get(self, "https_port")

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
    @pulumi.getter(name="originHostHeader")
    def origin_host_header(self) -> Optional[str]:
        """
        The host header value sent to the origin with each request. If you leave this blank, the request hostname determines this value. Azure CDN origins, such as Web Apps, Blob Storage, and Cloud Services require this host header value to match the origin hostname by default. This overrides the host header defined at Endpoint
        """
        return pulumi.get(self, "origin_host_header")

    @property
    @pulumi.getter
    def priority(self) -> Optional[int]:
        """
        Priority of origin in given origin group for load balancing. Higher priorities will not be used for load balancing if any lower priority origin is healthy.Must be between 1 and 5
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning status
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="sharedPrivateLinkResource")
    def shared_private_link_resource(self) -> Optional[Sequence['outputs.SharedPrivateLinkResourcePropertiesResponse']]:
        """
        The properties of the private link resource for private origin.
        """
        return pulumi.get(self, "shared_private_link_resource")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Read only system data
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def weight(self) -> Optional[int]:
        """
        Weight of the origin in given origin group for load balancing. Must be between 1 and 1000
        """
        return pulumi.get(self, "weight")


class AwaitableGetAFDOriginResult(GetAFDOriginResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAFDOriginResult(
            azure_origin=self.azure_origin,
            deployment_status=self.deployment_status,
            enabled_state=self.enabled_state,
            host_name=self.host_name,
            http_port=self.http_port,
            https_port=self.https_port,
            id=self.id,
            name=self.name,
            origin_host_header=self.origin_host_header,
            priority=self.priority,
            provisioning_state=self.provisioning_state,
            shared_private_link_resource=self.shared_private_link_resource,
            system_data=self.system_data,
            type=self.type,
            weight=self.weight)


def get_afd_origin(origin_group_name: Optional[str] = None,
                   origin_name: Optional[str] = None,
                   profile_name: Optional[str] = None,
                   resource_group_name: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAFDOriginResult:
    """
    Use this data source to access information about an existing resource.

    :param str origin_group_name: Name of the origin group which is unique within the profile.
    :param str origin_name: Name of the origin which is unique within the profile.
    :param str profile_name: Name of the CDN profile which is unique within the resource group.
    :param str resource_group_name: Name of the Resource group within the Azure subscription.
    """
    __args__ = dict()
    __args__['originGroupName'] = origin_group_name
    __args__['originName'] = origin_name
    __args__['profileName'] = profile_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:cdn/v20200901:getAFDOrigin', __args__, opts=opts, typ=GetAFDOriginResult).value

    return AwaitableGetAFDOriginResult(
        azure_origin=__ret__.azure_origin,
        deployment_status=__ret__.deployment_status,
        enabled_state=__ret__.enabled_state,
        host_name=__ret__.host_name,
        http_port=__ret__.http_port,
        https_port=__ret__.https_port,
        id=__ret__.id,
        name=__ret__.name,
        origin_host_header=__ret__.origin_host_header,
        priority=__ret__.priority,
        provisioning_state=__ret__.provisioning_state,
        shared_private_link_resource=__ret__.shared_private_link_resource,
        system_data=__ret__.system_data,
        type=__ret__.type,
        weight=__ret__.weight)
