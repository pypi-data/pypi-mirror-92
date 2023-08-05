# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['VpnConnection']


class VpnConnection(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection_name: Optional[pulumi.Input[str]] = None,
                 enable_bgp: Optional[pulumi.Input[bool]] = None,
                 gateway_name: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ipsec_policies: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IpsecPolicyArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 remote_vpn_site: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 routing_weight: Optional[pulumi.Input[int]] = None,
                 shared_key: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        VpnConnection Resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] connection_name: The name of the connection.
        :param pulumi.Input[bool] enable_bgp: EnableBgp flag
        :param pulumi.Input[str] gateway_name: The name of the gateway.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IpsecPolicyArgs']]]] ipsec_policies: The IPSec Policies to be considered by this connection.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input[pulumi.InputType['SubResourceArgs']] remote_vpn_site: Id of the connected vpn site.
        :param pulumi.Input[str] resource_group_name: The resource group name of the VpnGateway.
        :param pulumi.Input[int] routing_weight: routing weight for vpn connection.
        :param pulumi.Input[str] shared_key: SharedKey for the vpn connection.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            if connection_name is None and not opts.urn:
                raise TypeError("Missing required property 'connection_name'")
            __props__['connection_name'] = connection_name
            __props__['enable_bgp'] = enable_bgp
            if gateway_name is None and not opts.urn:
                raise TypeError("Missing required property 'gateway_name'")
            __props__['gateway_name'] = gateway_name
            __props__['id'] = id
            __props__['ipsec_policies'] = ipsec_policies
            __props__['name'] = name
            __props__['remote_vpn_site'] = remote_vpn_site
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['routing_weight'] = routing_weight
            __props__['shared_key'] = shared_key
            __props__['connection_bandwidth'] = None
            __props__['connection_status'] = None
            __props__['egress_bytes_transferred'] = None
            __props__['etag'] = None
            __props__['ingress_bytes_transferred'] = None
            __props__['provisioning_state'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:network/latest:VpnConnection"), pulumi.Alias(type_="azure-nextgen:network/v20180601:VpnConnection"), pulumi.Alias(type_="azure-nextgen:network/v20180701:VpnConnection"), pulumi.Alias(type_="azure-nextgen:network/v20180801:VpnConnection"), pulumi.Alias(type_="azure-nextgen:network/v20181001:VpnConnection"), pulumi.Alias(type_="azure-nextgen:network/v20181101:VpnConnection"), pulumi.Alias(type_="azure-nextgen:network/v20181201:VpnConnection"), pulumi.Alias(type_="azure-nextgen:network/v20190201:VpnConnection"), pulumi.Alias(type_="azure-nextgen:network/v20190401:VpnConnection"), pulumi.Alias(type_="azure-nextgen:network/v20190601:VpnConnection"), pulumi.Alias(type_="azure-nextgen:network/v20190701:VpnConnection"), pulumi.Alias(type_="azure-nextgen:network/v20190801:VpnConnection"), pulumi.Alias(type_="azure-nextgen:network/v20190901:VpnConnection"), pulumi.Alias(type_="azure-nextgen:network/v20191101:VpnConnection"), pulumi.Alias(type_="azure-nextgen:network/v20191201:VpnConnection"), pulumi.Alias(type_="azure-nextgen:network/v20200301:VpnConnection"), pulumi.Alias(type_="azure-nextgen:network/v20200401:VpnConnection"), pulumi.Alias(type_="azure-nextgen:network/v20200501:VpnConnection"), pulumi.Alias(type_="azure-nextgen:network/v20200601:VpnConnection"), pulumi.Alias(type_="azure-nextgen:network/v20200701:VpnConnection"), pulumi.Alias(type_="azure-nextgen:network/v20200801:VpnConnection")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(VpnConnection, __self__).__init__(
            'azure-nextgen:network/v20180401:VpnConnection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'VpnConnection':
        """
        Get an existing VpnConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return VpnConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="connectionBandwidth")
    def connection_bandwidth(self) -> pulumi.Output[int]:
        """
        Expected bandwidth in MBPS.
        """
        return pulumi.get(self, "connection_bandwidth")

    @property
    @pulumi.getter(name="connectionStatus")
    def connection_status(self) -> pulumi.Output[str]:
        """
        The connection status.
        """
        return pulumi.get(self, "connection_status")

    @property
    @pulumi.getter(name="egressBytesTransferred")
    def egress_bytes_transferred(self) -> pulumi.Output[float]:
        """
        Egress bytes transferred.
        """
        return pulumi.get(self, "egress_bytes_transferred")

    @property
    @pulumi.getter(name="enableBgp")
    def enable_bgp(self) -> pulumi.Output[Optional[bool]]:
        """
        EnableBgp flag
        """
        return pulumi.get(self, "enable_bgp")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        Gets a unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="ingressBytesTransferred")
    def ingress_bytes_transferred(self) -> pulumi.Output[float]:
        """
        Ingress bytes transferred.
        """
        return pulumi.get(self, "ingress_bytes_transferred")

    @property
    @pulumi.getter(name="ipsecPolicies")
    def ipsec_policies(self) -> pulumi.Output[Optional[Sequence['outputs.IpsecPolicyResponse']]]:
        """
        The IPSec Policies to be considered by this connection.
        """
        return pulumi.get(self, "ipsec_policies")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="remoteVpnSite")
    def remote_vpn_site(self) -> pulumi.Output[Optional['outputs.SubResourceResponse']]:
        """
        Id of the connected vpn site.
        """
        return pulumi.get(self, "remote_vpn_site")

    @property
    @pulumi.getter(name="routingWeight")
    def routing_weight(self) -> pulumi.Output[Optional[int]]:
        """
        routing weight for vpn connection.
        """
        return pulumi.get(self, "routing_weight")

    @property
    @pulumi.getter(name="sharedKey")
    def shared_key(self) -> pulumi.Output[Optional[str]]:
        """
        SharedKey for the vpn connection.
        """
        return pulumi.get(self, "shared_key")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

