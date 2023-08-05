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

__all__ = ['VirtualHubIpConfiguration']


class VirtualHubIpConfiguration(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 ip_config_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 private_ip_address: Optional[pulumi.Input[str]] = None,
                 private_ip_allocation_method: Optional[pulumi.Input[Union[str, 'IPAllocationMethod']]] = None,
                 public_ip_address: Optional[pulumi.Input[pulumi.InputType['PublicIPAddressArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 subnet: Optional[pulumi.Input[pulumi.InputType['SubnetArgs']]] = None,
                 virtual_hub_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        IpConfigurations.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] ip_config_name: The name of the ipconfig.
        :param pulumi.Input[str] name: Name of the Ip Configuration.
        :param pulumi.Input[str] private_ip_address: The private IP address of the IP configuration.
        :param pulumi.Input[Union[str, 'IPAllocationMethod']] private_ip_allocation_method: The private IP address allocation method.
        :param pulumi.Input[pulumi.InputType['PublicIPAddressArgs']] public_ip_address: The reference to the public IP resource.
        :param pulumi.Input[str] resource_group_name: The resource group name of the VirtualHub.
        :param pulumi.Input[pulumi.InputType['SubnetArgs']] subnet: The reference to the subnet resource.
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

            __props__['id'] = id
            if ip_config_name is None and not opts.urn:
                raise TypeError("Missing required property 'ip_config_name'")
            __props__['ip_config_name'] = ip_config_name
            __props__['name'] = name
            __props__['private_ip_address'] = private_ip_address
            __props__['private_ip_allocation_method'] = private_ip_allocation_method
            __props__['public_ip_address'] = public_ip_address
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['subnet'] = subnet
            if virtual_hub_name is None and not opts.urn:
                raise TypeError("Missing required property 'virtual_hub_name'")
            __props__['virtual_hub_name'] = virtual_hub_name
            __props__['etag'] = None
            __props__['provisioning_state'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:network/latest:VirtualHubIpConfiguration"), pulumi.Alias(type_="azure-nextgen:network/v20200501:VirtualHubIpConfiguration"), pulumi.Alias(type_="azure-nextgen:network/v20200601:VirtualHubIpConfiguration"), pulumi.Alias(type_="azure-nextgen:network/v20200801:VirtualHubIpConfiguration")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(VirtualHubIpConfiguration, __self__).__init__(
            'azure-nextgen:network/v20200701:VirtualHubIpConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'VirtualHubIpConfiguration':
        """
        Get an existing VirtualHubIpConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return VirtualHubIpConfiguration(resource_name, opts=opts, __props__=__props__)

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
        Name of the Ip Configuration.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateIPAddress")
    def private_ip_address(self) -> pulumi.Output[Optional[str]]:
        """
        The private IP address of the IP configuration.
        """
        return pulumi.get(self, "private_ip_address")

    @property
    @pulumi.getter(name="privateIPAllocationMethod")
    def private_ip_allocation_method(self) -> pulumi.Output[Optional[str]]:
        """
        The private IP address allocation method.
        """
        return pulumi.get(self, "private_ip_allocation_method")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the IP configuration resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publicIPAddress")
    def public_ip_address(self) -> pulumi.Output[Optional['outputs.PublicIPAddressResponse']]:
        """
        The reference to the public IP resource.
        """
        return pulumi.get(self, "public_ip_address")

    @property
    @pulumi.getter
    def subnet(self) -> pulumi.Output[Optional['outputs.SubnetResponse']]:
        """
        The reference to the subnet resource.
        """
        return pulumi.get(self, "subnet")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Ipconfiguration type.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

