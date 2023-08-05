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

__all__ = ['Subnet']


class Subnet(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 address_prefix: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_security_group: Optional[pulumi.Input[pulumi.InputType['NetworkSecurityGroupArgs']]] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_navigation_links: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResourceNavigationLinkArgs']]]]] = None,
                 route_table: Optional[pulumi.Input[pulumi.InputType['RouteTableArgs']]] = None,
                 service_endpoints: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ServiceEndpointPropertiesFormatArgs']]]]] = None,
                 subnet_name: Optional[pulumi.Input[str]] = None,
                 virtual_network_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Subnet in a virtual network resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] address_prefix: The address prefix for the subnet.
        :param pulumi.Input[str] etag: A unique read-only string that changes whenever the resource is updated.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input[pulumi.InputType['NetworkSecurityGroupArgs']] network_security_group: The reference of the NetworkSecurityGroup resource.
        :param pulumi.Input[str] provisioning_state: The provisioning state of the resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ResourceNavigationLinkArgs']]]] resource_navigation_links: Gets an array of references to the external resources using subnet.
        :param pulumi.Input[pulumi.InputType['RouteTableArgs']] route_table: The reference of the RouteTable resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ServiceEndpointPropertiesFormatArgs']]]] service_endpoints: An array of service endpoints.
        :param pulumi.Input[str] subnet_name: The name of the subnet.
        :param pulumi.Input[str] virtual_network_name: The name of the virtual network.
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

            __props__['address_prefix'] = address_prefix
            __props__['etag'] = etag
            __props__['id'] = id
            __props__['name'] = name
            __props__['network_security_group'] = network_security_group
            __props__['provisioning_state'] = provisioning_state
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['resource_navigation_links'] = resource_navigation_links
            __props__['route_table'] = route_table
            __props__['service_endpoints'] = service_endpoints
            if subnet_name is None and not opts.urn:
                raise TypeError("Missing required property 'subnet_name'")
            __props__['subnet_name'] = subnet_name
            if virtual_network_name is None and not opts.urn:
                raise TypeError("Missing required property 'virtual_network_name'")
            __props__['virtual_network_name'] = virtual_network_name
            __props__['ip_configurations'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:network/latest:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20150501preview:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20150615:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20160330:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20160601:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20160901:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20161201:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20170301:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20170601:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20170801:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20170901:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20171001:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20171101:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20180101:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20180401:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20180601:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20180701:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20180801:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20181001:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20181101:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20181201:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20190201:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20190401:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20190601:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20190701:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20190801:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20190901:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20191101:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20191201:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20200301:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20200401:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20200501:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20200601:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20200701:Subnet"), pulumi.Alias(type_="azure-nextgen:network/v20200801:Subnet")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Subnet, __self__).__init__(
            'azure-nextgen:network/v20180201:Subnet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Subnet':
        """
        Get an existing Subnet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Subnet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="addressPrefix")
    def address_prefix(self) -> pulumi.Output[Optional[str]]:
        """
        The address prefix for the subnet.
        """
        return pulumi.get(self, "address_prefix")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="ipConfigurations")
    def ip_configurations(self) -> pulumi.Output[Sequence['outputs.IPConfigurationResponse']]:
        """
        Gets an array of references to the network interface IP configurations using subnet.
        """
        return pulumi.get(self, "ip_configurations")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkSecurityGroup")
    def network_security_group(self) -> pulumi.Output[Optional['outputs.NetworkSecurityGroupResponse']]:
        """
        The reference of the NetworkSecurityGroup resource.
        """
        return pulumi.get(self, "network_security_group")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        The provisioning state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceNavigationLinks")
    def resource_navigation_links(self) -> pulumi.Output[Optional[Sequence['outputs.ResourceNavigationLinkResponse']]]:
        """
        Gets an array of references to the external resources using subnet.
        """
        return pulumi.get(self, "resource_navigation_links")

    @property
    @pulumi.getter(name="routeTable")
    def route_table(self) -> pulumi.Output[Optional['outputs.RouteTableResponse']]:
        """
        The reference of the RouteTable resource.
        """
        return pulumi.get(self, "route_table")

    @property
    @pulumi.getter(name="serviceEndpoints")
    def service_endpoints(self) -> pulumi.Output[Optional[Sequence['outputs.ServiceEndpointPropertiesFormatResponse']]]:
        """
        An array of service endpoints.
        """
        return pulumi.get(self, "service_endpoints")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

