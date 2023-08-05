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

__all__ = ['AvailabilitySet']


class AvailabilitySet(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 availability_set_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 platform_fault_domain_count: Optional[pulumi.Input[int]] = None,
                 platform_update_domain_count: Optional[pulumi.Input[int]] = None,
                 proximity_placement_group: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 virtual_machines: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SubResourceArgs']]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Specifies information about the availability set that the virtual machine should be assigned to. Virtual machines specified in the same availability set are allocated to different nodes to maximize availability. For more information about availability sets, see [Manage the availability of virtual machines](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-manage-availability?toc=%2fazure%2fvirtual-machines%2fwindows%2ftoc.json). <br><br> For more information on Azure planned maintenance, see [Planned maintenance for virtual machines in Azure](https://docs.microsoft.com/azure/virtual-machines/virtual-machines-windows-planned-maintenance?toc=%2fazure%2fvirtual-machines%2fwindows%2ftoc.json) <br><br> Currently, a VM can only be added to availability set at creation time. An existing VM cannot be added to an availability set.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] availability_set_name: The name of the availability set.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[int] platform_fault_domain_count: Fault Domain count.
        :param pulumi.Input[int] platform_update_domain_count: Update Domain count.
        :param pulumi.Input[pulumi.InputType['SubResourceArgs']] proximity_placement_group: Specifies information about the proximity placement group that the availability set should be assigned to. <br><br>Minimum api-version: 2018-04-01.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: Sku of the availability set
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['SubResourceArgs']]]] virtual_machines: A list of references to all virtual machines in the availability set.
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

            if availability_set_name is None and not opts.urn:
                raise TypeError("Missing required property 'availability_set_name'")
            __props__['availability_set_name'] = availability_set_name
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__['location'] = location
            __props__['platform_fault_domain_count'] = platform_fault_domain_count
            __props__['platform_update_domain_count'] = platform_update_domain_count
            __props__['proximity_placement_group'] = proximity_placement_group
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['sku'] = sku
            __props__['tags'] = tags
            __props__['virtual_machines'] = virtual_machines
            __props__['name'] = None
            __props__['statuses'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:compute/latest:AvailabilitySet"), pulumi.Alias(type_="azure-nextgen:compute/v20150615:AvailabilitySet"), pulumi.Alias(type_="azure-nextgen:compute/v20160330:AvailabilitySet"), pulumi.Alias(type_="azure-nextgen:compute/v20160430preview:AvailabilitySet"), pulumi.Alias(type_="azure-nextgen:compute/v20170330:AvailabilitySet"), pulumi.Alias(type_="azure-nextgen:compute/v20171201:AvailabilitySet"), pulumi.Alias(type_="azure-nextgen:compute/v20180601:AvailabilitySet"), pulumi.Alias(type_="azure-nextgen:compute/v20181001:AvailabilitySet"), pulumi.Alias(type_="azure-nextgen:compute/v20190301:AvailabilitySet"), pulumi.Alias(type_="azure-nextgen:compute/v20190701:AvailabilitySet"), pulumi.Alias(type_="azure-nextgen:compute/v20191201:AvailabilitySet"), pulumi.Alias(type_="azure-nextgen:compute/v20200601:AvailabilitySet")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(AvailabilitySet, __self__).__init__(
            'azure-nextgen:compute/v20180401:AvailabilitySet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AvailabilitySet':
        """
        Get an existing AvailabilitySet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return AvailabilitySet(resource_name, opts=opts, __props__=__props__)

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
    @pulumi.getter(name="platformFaultDomainCount")
    def platform_fault_domain_count(self) -> pulumi.Output[Optional[int]]:
        """
        Fault Domain count.
        """
        return pulumi.get(self, "platform_fault_domain_count")

    @property
    @pulumi.getter(name="platformUpdateDomainCount")
    def platform_update_domain_count(self) -> pulumi.Output[Optional[int]]:
        """
        Update Domain count.
        """
        return pulumi.get(self, "platform_update_domain_count")

    @property
    @pulumi.getter(name="proximityPlacementGroup")
    def proximity_placement_group(self) -> pulumi.Output[Optional['outputs.SubResourceResponse']]:
        """
        Specifies information about the proximity placement group that the availability set should be assigned to. <br><br>Minimum api-version: 2018-04-01.
        """
        return pulumi.get(self, "proximity_placement_group")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuResponse']]:
        """
        Sku of the availability set
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def statuses(self) -> pulumi.Output[Sequence['outputs.InstanceViewStatusResponse']]:
        """
        The resource status information.
        """
        return pulumi.get(self, "statuses")

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

    @property
    @pulumi.getter(name="virtualMachines")
    def virtual_machines(self) -> pulumi.Output[Optional[Sequence['outputs.SubResourceResponse']]]:
        """
        A list of references to all virtual machines in the availability set.
        """
        return pulumi.get(self, "virtual_machines")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

