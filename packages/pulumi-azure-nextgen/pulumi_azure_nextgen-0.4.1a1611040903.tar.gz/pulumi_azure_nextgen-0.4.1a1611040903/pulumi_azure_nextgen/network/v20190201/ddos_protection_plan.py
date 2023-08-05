# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs

__all__ = ['DdosProtectionPlan']


class DdosProtectionPlan(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 ddos_protection_plan_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A DDoS protection plan in a resource group.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] ddos_protection_plan_name: The name of the DDoS protection plan.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
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

            if ddos_protection_plan_name is None and not opts.urn:
                raise TypeError("Missing required property 'ddos_protection_plan_name'")
            __props__['ddos_protection_plan_name'] = ddos_protection_plan_name
            __props__['location'] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['tags'] = tags
            __props__['etag'] = None
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['resource_guid'] = None
            __props__['type'] = None
            __props__['virtual_networks'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:network/latest:DdosProtectionPlan"), pulumi.Alias(type_="azure-nextgen:network/v20180201:DdosProtectionPlan"), pulumi.Alias(type_="azure-nextgen:network/v20180401:DdosProtectionPlan"), pulumi.Alias(type_="azure-nextgen:network/v20180601:DdosProtectionPlan"), pulumi.Alias(type_="azure-nextgen:network/v20180701:DdosProtectionPlan"), pulumi.Alias(type_="azure-nextgen:network/v20180801:DdosProtectionPlan"), pulumi.Alias(type_="azure-nextgen:network/v20181001:DdosProtectionPlan"), pulumi.Alias(type_="azure-nextgen:network/v20181101:DdosProtectionPlan"), pulumi.Alias(type_="azure-nextgen:network/v20181201:DdosProtectionPlan"), pulumi.Alias(type_="azure-nextgen:network/v20190401:DdosProtectionPlan"), pulumi.Alias(type_="azure-nextgen:network/v20190601:DdosProtectionPlan"), pulumi.Alias(type_="azure-nextgen:network/v20190701:DdosProtectionPlan"), pulumi.Alias(type_="azure-nextgen:network/v20190801:DdosProtectionPlan"), pulumi.Alias(type_="azure-nextgen:network/v20190901:DdosProtectionPlan"), pulumi.Alias(type_="azure-nextgen:network/v20191101:DdosProtectionPlan"), pulumi.Alias(type_="azure-nextgen:network/v20191201:DdosProtectionPlan"), pulumi.Alias(type_="azure-nextgen:network/v20200301:DdosProtectionPlan"), pulumi.Alias(type_="azure-nextgen:network/v20200401:DdosProtectionPlan"), pulumi.Alias(type_="azure-nextgen:network/v20200501:DdosProtectionPlan"), pulumi.Alias(type_="azure-nextgen:network/v20200601:DdosProtectionPlan"), pulumi.Alias(type_="azure-nextgen:network/v20200701:DdosProtectionPlan"), pulumi.Alias(type_="azure-nextgen:network/v20200801:DdosProtectionPlan")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DdosProtectionPlan, __self__).__init__(
            'azure-nextgen:network/v20190201:DdosProtectionPlan',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DdosProtectionPlan':
        """
        Get an existing DdosProtectionPlan resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return DdosProtectionPlan(resource_name, opts=opts, __props__=__props__)

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
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the DDoS protection plan resource. Possible values are: 'Succeeded', 'Updating', 'Deleting', and 'Failed'.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceGuid")
    def resource_guid(self) -> pulumi.Output[str]:
        """
        The resource GUID property of the DDoS protection plan resource. It uniquely identifies the resource, even if the user changes its name or migrate the resource across subscriptions or resource groups.
        """
        return pulumi.get(self, "resource_guid")

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

    @property
    @pulumi.getter(name="virtualNetworks")
    def virtual_networks(self) -> pulumi.Output[Sequence['outputs.SubResourceResponse']]:
        """
        The list of virtual networks associated with the DDoS protection plan resource. This list is read-only.
        """
        return pulumi.get(self, "virtual_networks")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

