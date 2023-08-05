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

__all__ = ['PublicIpAddress']


class PublicIpAddress(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dns_settings: Optional[pulumi.Input[pulumi.InputType['PublicIpAddressDnsSettingsArgs']]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 idle_timeout_in_minutes: Optional[pulumi.Input[int]] = None,
                 ip_address: Optional[pulumi.Input[str]] = None,
                 ip_configuration: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 public_ip_allocation_method: Optional[pulumi.Input[Union[str, 'IpAllocationMethod']]] = None,
                 public_ip_address_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_guid: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        PublicIPAddress resource

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['PublicIpAddressDnsSettingsArgs']] dns_settings: Gets or sets FQDN of the DNS record associated with the public IP address
        :param pulumi.Input[str] etag: Gets a unique read-only string that changes whenever the resource is updated
        :param pulumi.Input[int] idle_timeout_in_minutes: Gets or sets the idle timeout of the public IP address
        :param pulumi.Input[str] ip_address: Gets the assigned public IP address
        :param pulumi.Input[pulumi.InputType['SubResourceArgs']] ip_configuration: Gets a reference to the network interface IP configurations using this public IP address
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] provisioning_state: Gets or sets Provisioning state of the PublicIP resource Updating/Deleting/Failed
        :param pulumi.Input[Union[str, 'IpAllocationMethod']] public_ip_allocation_method: Gets or sets PublicIP allocation method (Static/Dynamic)
        :param pulumi.Input[str] public_ip_address_name: The name of the publicIpAddress.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] resource_guid: Gets or sets resource guid property of the PublicIP resource
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
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

            __props__['dns_settings'] = dns_settings
            __props__['etag'] = etag
            __props__['idle_timeout_in_minutes'] = idle_timeout_in_minutes
            __props__['ip_address'] = ip_address
            __props__['ip_configuration'] = ip_configuration
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__['location'] = location
            __props__['provisioning_state'] = provisioning_state
            if public_ip_allocation_method is None and not opts.urn:
                raise TypeError("Missing required property 'public_ip_allocation_method'")
            __props__['public_ip_allocation_method'] = public_ip_allocation_method
            if public_ip_address_name is None and not opts.urn:
                raise TypeError("Missing required property 'public_ip_address_name'")
            __props__['public_ip_address_name'] = public_ip_address_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['resource_guid'] = resource_guid
            __props__['tags'] = tags
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:network/latest:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20150615:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20160330:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20160601:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20160901:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20161201:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20170301:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20170601:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20170801:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20170901:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20171001:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20171101:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20180101:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20180201:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20180401:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20180601:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20180701:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20180801:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20181001:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20181101:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20181201:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20190201:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20190401:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20190601:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20190701:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20190801:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20190901:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20191101:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20191201:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20200301:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20200401:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20200501:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20200601:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20200701:PublicIpAddress"), pulumi.Alias(type_="azure-nextgen:network/v20200801:PublicIpAddress")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(PublicIpAddress, __self__).__init__(
            'azure-nextgen:network/v20150501preview:PublicIpAddress',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'PublicIpAddress':
        """
        Get an existing PublicIpAddress resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return PublicIpAddress(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dnsSettings")
    def dns_settings(self) -> pulumi.Output[Optional['outputs.PublicIpAddressDnsSettingsResponse']]:
        """
        Gets or sets FQDN of the DNS record associated with the public IP address
        """
        return pulumi.get(self, "dns_settings")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        Gets a unique read-only string that changes whenever the resource is updated
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="idleTimeoutInMinutes")
    def idle_timeout_in_minutes(self) -> pulumi.Output[Optional[int]]:
        """
        Gets or sets the idle timeout of the public IP address
        """
        return pulumi.get(self, "idle_timeout_in_minutes")

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> pulumi.Output[Optional[str]]:
        """
        Gets the assigned public IP address
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter(name="ipConfiguration")
    def ip_configuration(self) -> pulumi.Output[Optional['outputs.SubResourceResponse']]:
        """
        Gets a reference to the network interface IP configurations using this public IP address
        """
        return pulumi.get(self, "ip_configuration")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets Provisioning state of the PublicIP resource Updating/Deleting/Failed
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publicIPAllocationMethod")
    def public_ip_allocation_method(self) -> pulumi.Output[str]:
        """
        Gets or sets PublicIP allocation method (Static/Dynamic)
        """
        return pulumi.get(self, "public_ip_allocation_method")

    @property
    @pulumi.getter(name="resourceGuid")
    def resource_guid(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets resource guid property of the PublicIP resource
        """
        return pulumi.get(self, "resource_guid")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

