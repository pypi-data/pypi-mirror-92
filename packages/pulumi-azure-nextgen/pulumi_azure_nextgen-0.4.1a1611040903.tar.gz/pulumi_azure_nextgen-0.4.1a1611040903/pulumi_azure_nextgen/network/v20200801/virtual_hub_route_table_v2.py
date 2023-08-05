# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs
from ._inputs import *

__all__ = ['VirtualHubRouteTableV2']


class VirtualHubRouteTableV2(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attached_connections: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 route_table_name: Optional[pulumi.Input[str]] = None,
                 routes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualHubRouteV2Args']]]]] = None,
                 virtual_hub_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        VirtualHubRouteTableV2 Resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] attached_connections: List of all connections attached to this route table v2.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input[str] resource_group_name: The resource group name of the VirtualHub.
        :param pulumi.Input[str] route_table_name: The name of the VirtualHubRouteTableV2.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VirtualHubRouteV2Args']]]] routes: List of all routes.
        :param pulumi.Input[str] virtual_hub_name: The name of the VirtualHub.
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

            __props__['attached_connections'] = attached_connections
            __props__['id'] = id
            __props__['name'] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if route_table_name is None and not opts.urn:
                raise TypeError("Missing required property 'route_table_name'")
            __props__['route_table_name'] = route_table_name
            __props__['routes'] = routes
            if virtual_hub_name is None and not opts.urn:
                raise TypeError("Missing required property 'virtual_hub_name'")
            __props__['virtual_hub_name'] = virtual_hub_name
            __props__['etag'] = None
            __props__['provisioning_state'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:network/latest:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-nextgen:network/v20190901:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-nextgen:network/v20191101:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-nextgen:network/v20191201:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-nextgen:network/v20200301:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-nextgen:network/v20200401:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-nextgen:network/v20200501:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-nextgen:network/v20200601:VirtualHubRouteTableV2"), pulumi.Alias(type_="azure-nextgen:network/v20200701:VirtualHubRouteTableV2")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(VirtualHubRouteTableV2, __self__).__init__(
            'azure-nextgen:network/v20200801:VirtualHubRouteTableV2',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'VirtualHubRouteTableV2':
        """
        Get an existing VirtualHubRouteTableV2 resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return VirtualHubRouteTableV2(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="attachedConnections")
    def attached_connections(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        List of all connections attached to this route table v2.
        """
        return pulumi.get(self, "attached_connections")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

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
        The provisioning state of the virtual hub route table v2 resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def routes(self) -> pulumi.Output[Optional[Sequence['outputs.VirtualHubRouteV2Response']]]:
        """
        List of all routes.
        """
        return pulumi.get(self, "routes")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

