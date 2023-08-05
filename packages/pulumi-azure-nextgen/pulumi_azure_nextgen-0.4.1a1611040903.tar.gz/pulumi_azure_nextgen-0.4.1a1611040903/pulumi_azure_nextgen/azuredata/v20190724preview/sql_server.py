# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = ['SqlServer']


class SqlServer(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cores: Optional[pulumi.Input[int]] = None,
                 edition: Optional[pulumi.Input[str]] = None,
                 property_bag: Optional[pulumi.Input[str]] = None,
                 registration_id: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sql_server_name: Optional[pulumi.Input[str]] = None,
                 sql_server_registration_name: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A SQL server.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] cores: Cores of the Sql Server.
        :param pulumi.Input[str] edition: Sql Server Edition.
        :param pulumi.Input[str] property_bag: Sql Server Json Property Bag.
        :param pulumi.Input[str] registration_id: ID for Parent Sql Server Registration.
        :param pulumi.Input[str] resource_group_name: Name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] sql_server_name: Name of the SQL Server.
        :param pulumi.Input[str] sql_server_registration_name: Name of the SQL Server registration.
        :param pulumi.Input[str] version: Version of the Sql Server.
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

            __props__['cores'] = cores
            __props__['edition'] = edition
            __props__['property_bag'] = property_bag
            __props__['registration_id'] = registration_id
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if sql_server_name is None and not opts.urn:
                raise TypeError("Missing required property 'sql_server_name'")
            __props__['sql_server_name'] = sql_server_name
            if sql_server_registration_name is None and not opts.urn:
                raise TypeError("Missing required property 'sql_server_registration_name'")
            __props__['sql_server_registration_name'] = sql_server_registration_name
            __props__['version'] = version
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:azuredata/v20170301preview:SqlServer")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SqlServer, __self__).__init__(
            'azure-nextgen:azuredata/v20190724preview:SqlServer',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SqlServer':
        """
        Get an existing SqlServer resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return SqlServer(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def cores(self) -> pulumi.Output[Optional[int]]:
        """
        Cores of the Sql Server.
        """
        return pulumi.get(self, "cores")

    @property
    @pulumi.getter
    def edition(self) -> pulumi.Output[Optional[str]]:
        """
        Sql Server Edition.
        """
        return pulumi.get(self, "edition")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="propertyBag")
    def property_bag(self) -> pulumi.Output[Optional[str]]:
        """
        Sql Server Json Property Bag.
        """
        return pulumi.get(self, "property_bag")

    @property
    @pulumi.getter(name="registrationID")
    def registration_id(self) -> pulumi.Output[Optional[str]]:
        """
        ID for Parent Sql Server Registration.
        """
        return pulumi.get(self, "registration_id")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. Ex- Microsoft.Compute/virtualMachines or Microsoft.Storage/storageAccounts.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[Optional[str]]:
        """
        Version of the Sql Server.
        """
        return pulumi.get(self, "version")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

