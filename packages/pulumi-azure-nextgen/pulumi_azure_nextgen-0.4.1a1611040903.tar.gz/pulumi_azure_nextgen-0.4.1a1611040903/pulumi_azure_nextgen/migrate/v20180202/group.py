# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = ['Group']


class Group(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 e_tag: Optional[pulumi.Input[str]] = None,
                 group_name: Optional[pulumi.Input[str]] = None,
                 machines: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 project_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A group created in a Migration project.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] e_tag: For optimistic concurrency control.
        :param pulumi.Input[str] group_name: Unique name of a group within a project.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] machines: List of machine names that are part of this group.
        :param pulumi.Input[str] project_name: Name of the Azure Migrate project.
        :param pulumi.Input[str] resource_group_name: Name of the Azure Resource Group that project is part of.
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

            __props__['e_tag'] = e_tag
            if group_name is None and not opts.urn:
                raise TypeError("Missing required property 'group_name'")
            __props__['group_name'] = group_name
            if machines is None and not opts.urn:
                raise TypeError("Missing required property 'machines'")
            __props__['machines'] = machines
            if project_name is None and not opts.urn:
                raise TypeError("Missing required property 'project_name'")
            __props__['project_name'] = project_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['assessments'] = None
            __props__['created_timestamp'] = None
            __props__['name'] = None
            __props__['type'] = None
            __props__['updated_timestamp'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:migrate/v20171111preview:Group")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Group, __self__).__init__(
            'azure-nextgen:migrate/v20180202:Group',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Group':
        """
        Get an existing Group resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Group(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def assessments(self) -> pulumi.Output[Sequence[str]]:
        """
        List of References to Assessments created on this group.
        """
        return pulumi.get(self, "assessments")

    @property
    @pulumi.getter(name="createdTimestamp")
    def created_timestamp(self) -> pulumi.Output[str]:
        """
        Time when this project was created. Date-Time represented in ISO-8601 format.
        """
        return pulumi.get(self, "created_timestamp")

    @property
    @pulumi.getter(name="eTag")
    def e_tag(self) -> pulumi.Output[Optional[str]]:
        """
        For optimistic concurrency control.
        """
        return pulumi.get(self, "e_tag")

    @property
    @pulumi.getter
    def machines(self) -> pulumi.Output[Sequence[str]]:
        """
        List of machine names that are part of this group.
        """
        return pulumi.get(self, "machines")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the group.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of the object = [Microsoft.Migrate/projects/groups].
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="updatedTimestamp")
    def updated_timestamp(self) -> pulumi.Output[str]:
        """
        Time when this project was last updated. Date-Time represented in ISO-8601 format.
        """
        return pulumi.get(self, "updated_timestamp")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

