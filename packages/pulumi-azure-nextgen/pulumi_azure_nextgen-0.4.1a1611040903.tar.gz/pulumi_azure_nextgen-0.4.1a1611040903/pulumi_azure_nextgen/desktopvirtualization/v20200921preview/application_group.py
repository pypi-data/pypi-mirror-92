# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from ._enums import *

__all__ = ['ApplicationGroup']


class ApplicationGroup(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_group_name: Optional[pulumi.Input[str]] = None,
                 application_group_type: Optional[pulumi.Input[Union[str, 'ApplicationGroupType']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 friendly_name: Optional[pulumi.Input[str]] = None,
                 host_pool_arm_path: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Represents a ApplicationGroup definition.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application_group_name: The name of the application group
        :param pulumi.Input[Union[str, 'ApplicationGroupType']] application_group_type: Resource Type of ApplicationGroup.
        :param pulumi.Input[str] description: Description of ApplicationGroup.
        :param pulumi.Input[str] friendly_name: Friendly name of ApplicationGroup.
        :param pulumi.Input[str] host_pool_arm_path: HostPool arm path of ApplicationGroup.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
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

            if application_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'application_group_name'")
            __props__['application_group_name'] = application_group_name
            if application_group_type is None and not opts.urn:
                raise TypeError("Missing required property 'application_group_type'")
            __props__['application_group_type'] = application_group_type
            __props__['description'] = description
            __props__['friendly_name'] = friendly_name
            if host_pool_arm_path is None and not opts.urn:
                raise TypeError("Missing required property 'host_pool_arm_path'")
            __props__['host_pool_arm_path'] = host_pool_arm_path
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__['location'] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['tags'] = tags
            __props__['name'] = None
            __props__['type'] = None
            __props__['workspace_arm_path'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:desktopvirtualization/v20190123preview:ApplicationGroup"), pulumi.Alias(type_="azure-nextgen:desktopvirtualization/v20190924preview:ApplicationGroup"), pulumi.Alias(type_="azure-nextgen:desktopvirtualization/v20191210preview:ApplicationGroup"), pulumi.Alias(type_="azure-nextgen:desktopvirtualization/v20201019preview:ApplicationGroup"), pulumi.Alias(type_="azure-nextgen:desktopvirtualization/v20201102preview:ApplicationGroup"), pulumi.Alias(type_="azure-nextgen:desktopvirtualization/v20201110preview:ApplicationGroup")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ApplicationGroup, __self__).__init__(
            'azure-nextgen:desktopvirtualization/v20200921preview:ApplicationGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ApplicationGroup':
        """
        Get an existing ApplicationGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return ApplicationGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="applicationGroupType")
    def application_group_type(self) -> pulumi.Output[str]:
        """
        Resource Type of ApplicationGroup.
        """
        return pulumi.get(self, "application_group_type")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of ApplicationGroup.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> pulumi.Output[Optional[str]]:
        """
        Friendly name of ApplicationGroup.
        """
        return pulumi.get(self, "friendly_name")

    @property
    @pulumi.getter(name="hostPoolArmPath")
    def host_pool_arm_path(self) -> pulumi.Output[str]:
        """
        HostPool arm path of ApplicationGroup.
        """
        return pulumi.get(self, "host_pool_arm_path")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

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
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="workspaceArmPath")
    def workspace_arm_path(self) -> pulumi.Output[str]:
        """
        Workspace arm path of ApplicationGroup.
        """
        return pulumi.get(self, "workspace_arm_path")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

