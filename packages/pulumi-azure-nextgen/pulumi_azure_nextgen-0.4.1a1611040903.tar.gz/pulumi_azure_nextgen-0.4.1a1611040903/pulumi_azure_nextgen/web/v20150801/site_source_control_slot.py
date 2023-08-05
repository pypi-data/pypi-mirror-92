# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = ['SiteSourceControlSlot']


class SiteSourceControlSlot(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 branch: Optional[pulumi.Input[str]] = None,
                 deployment_rollback_enabled: Optional[pulumi.Input[bool]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 is_manual_integration: Optional[pulumi.Input[bool]] = None,
                 is_mercurial: Optional[pulumi.Input[bool]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 repo_url: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 slot: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Describes the source control configuration for web app

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] branch: Name of branch to use for deployment
        :param pulumi.Input[bool] deployment_rollback_enabled: Whether to manual or continuous integration
        :param pulumi.Input[str] id: Resource Id
        :param pulumi.Input[bool] is_manual_integration: Whether to manual or continuous integration
        :param pulumi.Input[bool] is_mercurial: Mercurial or Git repository type
        :param pulumi.Input[str] kind: Kind of resource
        :param pulumi.Input[str] location: Resource Location
        :param pulumi.Input[str] name: Resource Name
        :param pulumi.Input[str] repo_url: Repository or source control url
        :param pulumi.Input[str] resource_group_name: Name of resource group
        :param pulumi.Input[str] slot: Name of web app slot. If not specified then will default to production slot.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[str] type: Resource type
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

            __props__['branch'] = branch
            __props__['deployment_rollback_enabled'] = deployment_rollback_enabled
            __props__['id'] = id
            __props__['is_manual_integration'] = is_manual_integration
            __props__['is_mercurial'] = is_mercurial
            __props__['kind'] = kind
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__['location'] = location
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            __props__['repo_url'] = repo_url
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if slot is None and not opts.urn:
                raise TypeError("Missing required property 'slot'")
            __props__['slot'] = slot
            __props__['tags'] = tags
            __props__['type'] = type
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:web/latest:SiteSourceControlSlot"), pulumi.Alias(type_="azure-nextgen:web/v20160801:SiteSourceControlSlot"), pulumi.Alias(type_="azure-nextgen:web/v20180201:SiteSourceControlSlot"), pulumi.Alias(type_="azure-nextgen:web/v20181101:SiteSourceControlSlot"), pulumi.Alias(type_="azure-nextgen:web/v20190801:SiteSourceControlSlot"), pulumi.Alias(type_="azure-nextgen:web/v20200601:SiteSourceControlSlot"), pulumi.Alias(type_="azure-nextgen:web/v20200901:SiteSourceControlSlot")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SiteSourceControlSlot, __self__).__init__(
            'azure-nextgen:web/v20150801:SiteSourceControlSlot',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SiteSourceControlSlot':
        """
        Get an existing SiteSourceControlSlot resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return SiteSourceControlSlot(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def branch(self) -> pulumi.Output[Optional[str]]:
        """
        Name of branch to use for deployment
        """
        return pulumi.get(self, "branch")

    @property
    @pulumi.getter(name="deploymentRollbackEnabled")
    def deployment_rollback_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether to manual or continuous integration
        """
        return pulumi.get(self, "deployment_rollback_enabled")

    @property
    @pulumi.getter(name="isManualIntegration")
    def is_manual_integration(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether to manual or continuous integration
        """
        return pulumi.get(self, "is_manual_integration")

    @property
    @pulumi.getter(name="isMercurial")
    def is_mercurial(self) -> pulumi.Output[Optional[bool]]:
        """
        Mercurial or Git repository type
        """
        return pulumi.get(self, "is_mercurial")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource Location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        Resource Name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="repoUrl")
    def repo_url(self) -> pulumi.Output[Optional[str]]:
        """
        Repository or source control url
        """
        return pulumi.get(self, "repo_url")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[Optional[str]]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

