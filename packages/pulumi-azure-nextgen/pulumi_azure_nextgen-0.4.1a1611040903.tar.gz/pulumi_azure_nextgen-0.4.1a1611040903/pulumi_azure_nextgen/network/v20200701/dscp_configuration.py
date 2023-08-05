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

__all__ = ['DscpConfiguration']


class DscpConfiguration(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 destination_ip_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['QosIpRangeArgs']]]]] = None,
                 destination_port_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['QosPortRangeArgs']]]]] = None,
                 dscp_configuration_name: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 markings: Optional[pulumi.Input[Sequence[pulumi.Input[int]]]] = None,
                 protocol: Optional[pulumi.Input[Union[str, 'ProtocolType']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 source_ip_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['QosIpRangeArgs']]]]] = None,
                 source_port_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['QosPortRangeArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        DSCP Configuration in a resource group.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['QosIpRangeArgs']]]] destination_ip_ranges: Destination IP ranges.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['QosPortRangeArgs']]]] destination_port_ranges: Destination port ranges.
        :param pulumi.Input[str] dscp_configuration_name: The name of the resource.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[Sequence[pulumi.Input[int]]] markings: List of markings to be used in the configuration.
        :param pulumi.Input[Union[str, 'ProtocolType']] protocol: RNM supported protocol types.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['QosIpRangeArgs']]]] source_ip_ranges: Source IP ranges.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['QosPortRangeArgs']]]] source_port_ranges: Sources port ranges.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
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

            __props__['destination_ip_ranges'] = destination_ip_ranges
            __props__['destination_port_ranges'] = destination_port_ranges
            if dscp_configuration_name is None and not opts.urn:
                raise TypeError("Missing required property 'dscp_configuration_name'")
            __props__['dscp_configuration_name'] = dscp_configuration_name
            __props__['id'] = id
            __props__['location'] = location
            __props__['markings'] = markings
            __props__['protocol'] = protocol
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['source_ip_ranges'] = source_ip_ranges
            __props__['source_port_ranges'] = source_port_ranges
            __props__['tags'] = tags
            __props__['associated_network_interfaces'] = None
            __props__['etag'] = None
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['qos_collection_id'] = None
            __props__['resource_guid'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:network/latest:DscpConfiguration"), pulumi.Alias(type_="azure-nextgen:network/v20200601:DscpConfiguration"), pulumi.Alias(type_="azure-nextgen:network/v20200801:DscpConfiguration")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DscpConfiguration, __self__).__init__(
            'azure-nextgen:network/v20200701:DscpConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DscpConfiguration':
        """
        Get an existing DscpConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return DscpConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="associatedNetworkInterfaces")
    def associated_network_interfaces(self) -> pulumi.Output[Sequence['outputs.NetworkInterfaceResponse']]:
        """
        Associated Network Interfaces to the DSCP Configuration.
        """
        return pulumi.get(self, "associated_network_interfaces")

    @property
    @pulumi.getter(name="destinationIpRanges")
    def destination_ip_ranges(self) -> pulumi.Output[Optional[Sequence['outputs.QosIpRangeResponse']]]:
        """
        Destination IP ranges.
        """
        return pulumi.get(self, "destination_ip_ranges")

    @property
    @pulumi.getter(name="destinationPortRanges")
    def destination_port_ranges(self) -> pulumi.Output[Optional[Sequence['outputs.QosPortRangeResponse']]]:
        """
        Destination port ranges.
        """
        return pulumi.get(self, "destination_port_ranges")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def markings(self) -> pulumi.Output[Optional[Sequence[int]]]:
        """
        List of markings to be used in the configuration.
        """
        return pulumi.get(self, "markings")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Output[Optional[str]]:
        """
        RNM supported protocol types.
        """
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the DSCP Configuration resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="qosCollectionId")
    def qos_collection_id(self) -> pulumi.Output[str]:
        """
        Qos Collection ID generated by RNM.
        """
        return pulumi.get(self, "qos_collection_id")

    @property
    @pulumi.getter(name="resourceGuid")
    def resource_guid(self) -> pulumi.Output[str]:
        """
        The resource GUID property of the DSCP Configuration resource.
        """
        return pulumi.get(self, "resource_guid")

    @property
    @pulumi.getter(name="sourceIpRanges")
    def source_ip_ranges(self) -> pulumi.Output[Optional[Sequence['outputs.QosIpRangeResponse']]]:
        """
        Source IP ranges.
        """
        return pulumi.get(self, "source_ip_ranges")

    @property
    @pulumi.getter(name="sourcePortRanges")
    def source_port_ranges(self) -> pulumi.Output[Optional[Sequence['outputs.QosPortRangeResponse']]]:
        """
        Sources port ranges.
        """
        return pulumi.get(self, "source_port_ranges")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

