# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = ['ManagedInstanceAzureADOnlyAuthentication']


class ManagedInstanceAzureADOnlyAuthentication(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authentication_name: Optional[pulumi.Input[str]] = None,
                 azure_ad_only_authentication: Optional[pulumi.Input[bool]] = None,
                 managed_instance_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Azure Active Directory only authentication.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authentication_name: The name of server azure active directory only authentication.
        :param pulumi.Input[bool] azure_ad_only_authentication: Azure Active Directory only Authentication enabled.
        :param pulumi.Input[str] managed_instance_name: The name of the managed instance.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
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

            if authentication_name is None and not opts.urn:
                raise TypeError("Missing required property 'authentication_name'")
            __props__['authentication_name'] = authentication_name
            if azure_ad_only_authentication is None and not opts.urn:
                raise TypeError("Missing required property 'azure_ad_only_authentication'")
            __props__['azure_ad_only_authentication'] = azure_ad_only_authentication
            if managed_instance_name is None and not opts.urn:
                raise TypeError("Missing required property 'managed_instance_name'")
            __props__['managed_instance_name'] = managed_instance_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:sql/v20200202preview:ManagedInstanceAzureADOnlyAuthentication")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ManagedInstanceAzureADOnlyAuthentication, __self__).__init__(
            'azure-nextgen:sql/v20200801preview:ManagedInstanceAzureADOnlyAuthentication',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ManagedInstanceAzureADOnlyAuthentication':
        """
        Get an existing ManagedInstanceAzureADOnlyAuthentication resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return ManagedInstanceAzureADOnlyAuthentication(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="azureADOnlyAuthentication")
    def azure_ad_only_authentication(self) -> pulumi.Output[bool]:
        """
        Azure Active Directory only Authentication enabled.
        """
        return pulumi.get(self, "azure_ad_only_authentication")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

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

